import law
import luigi
import pickle
import numpy as np
import json
import os
import re
from itertools import combinations
from tasks.combine import CombineBase, ScanSingles, POITask, ScanAll, Impacts
from getPOIs import GetT2WOpts, GetPOIsList
from tasks.utils import ScanMethod
from interpolator.base import rbfInterpolator
from interpolator.utils import Data
from interpolator.profiler import profile1D, profile2D
from simplified.base import Approximator, SimplifedInterpolator
from law.logger import get_logger
logger = get_logger('luigi-interface')

class BuildInterpolated(CombineBase):
    def requires(self):
        return ScanAll.req(self)

    def output(self):
        return self.local_target(f"interp.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.pkl")
    
    def run(self):
        inputs = self.requires().input()['all']
        assert isinstance(inputs, law.LocalFileTarget)
        
        # Construct the interpolator
        logger.info(f"Building interpolator for {inputs.path}")
        interp = rbfInterpolator(inputs.path)
        pois = self.COMBINE_POIS.split(',')
        bounds = self.bounds
        data_config = Data(
            channel=self.channel,
            model=self.model,
            type=self.types,
            attribute=self.attributes,
            POIs={poi: {'bounds': bound} for poi, bound in zip(pois, bounds)},
            interpolator={"mode": "RBF", "eps_range": [(0.1, 100)]},
            splitting="grid",
            fraction=1.0,
            subtractbest=False
        )

        # Find the best value of eps
        logger.info(f"Finding best value of epsilon")
        interp.initialise(data_config)
        
        # Pickle the interpolator
        logger.info(f"Pickling interpolator to {self.output().path}")
        with open(self.output().path, 'wb') as f:
            pickle.dump(interp, f)
        logger.info(f"Interpolator built")

class BuildSimplified(CombineBase):
    parametrisation = luigi.Parameter(
        description="The parametrisation to use. Must be a key defined in simplified_dict."
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.approximation = simplified_configs[self.parametrisation]
            if self.approximation.model is None:
                self.approximation.model = self.model
        except KeyError:
            raise KeyError(f"Approximation {self.parametrisation} not found in {simplified_configs.keys()}")

    def requires(self):
        return {
            'impacts' : Impacts.req(self, **self.approximation.to_params()),
            'singles' : ScanSingles.req(self, **self.approximation.to_params()),
        }
    
    def output(self):
        return self.local_target(f"simplified.{self.channel}.{self.approximation.model}.{self.types}.pkl")
    
    def run(self):
        # Construct the interpolator
        logger.info(f"Building interpolator for {self.approximation.to_params()}")
        linear = True if 'linear' in self.model.lower() else False
        logger.info(f"Setting linear to {linear} for model {self.model}")
    
        # Construct mu_opts
        mu_opts = {
            'model': self.approximation.model,
            'limit_json': self.requires()['singles'].output()['limits'].path,
            'model_pois': GetPOIsList(self.approximation.model).split(','),
            'hesse_path': self.requires()['impacts'].output()["collection"].targets[0]['robustHesse'].path,
            'bins_path': os.getenv('ANALYSIS_PATH'),
            'needs_rot': self.approximation.needs_rot
        }
        
        # Get any --PO args in the wsp_opts string
        wsp_opts = GetT2WOpts(self.model)
        po_args = re.findall(r"--PO (.+?) ", wsp_opts)
        # Get the value of any po_arg with 'parametrisation' in it
        parametrisation = [po_arg.split("=")[-1] for po_arg in po_args if 'parametrisation' in po_arg]
        assert len(parametrisation) <= 1, f"Expected at most one parametrisation argument, got {parametrisation}"
        if len(parametrisation) == 0:
            parametrisation = ['CMS-prelim-SMEFT-topU3l_22_05_05_AccCorr_0p01']
            logger.warning(f"No parametrisation argument found in T2WOpts, using default: {parametrisation[0]}")
        
        mu_opts['EFT_parametrisation_path'] = os.path.join(os.getenv("CMSSW_BASE"), 'src', 'HiggsAnalysis', 
                                                                     'CombinedLimit', 'data', 'eft', 'STXStoSMEFT',
                                                                     parametrisation[0])
        
        # Construct the interpolator
        interp = SimplifedInterpolator(self.COMBINE_POIS.split(','), self.bounds, linear, mu_opts)
        
        # Pickle the interpolator
        logger.info(f"Pickling interpolator to {self.output().path}")
        with open(self.output().path, 'wb') as f:
            pickle.dump(interp, f)
        logger.info(f"Interpolator built")

# TODO refactor so all the dicts are in the same place
approximator_types = {
    'interpolated': BuildInterpolated,
    'simplified': BuildSimplified,
}
simplified_configs = { # TODO make this non-hgg specific
    "STXS" : Approximator(
        model="STXSStage1p2XSBRRefHggStatOnly",
        needs_rot=True,
        ),
    "SMEFT" : Approximator(
        model=None, # passthru
        needs_rot=False,
    )
}

class ApproximateBase(CombineBase):
    approximator_type = luigi.Parameter(
        description="The type of approximator to use. Must be a key defined in approximator_types."
    )
    approximation_parametrisation = luigi.OptionalParameter(
        description="The approximation to use. Must be a key defined in simplified_dict. Only used for 'simplified' approximators.",
        default=None
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.approximator_type == 'simplified':
            assert self.approximation_parametrisation is not None, f"Approximation parametrisation must be provided for simplified approximators"
        self.approximator = ApproximatorFactory.create(self.approximator_type, 
                                                       self.approximation_parametrisation)
        
        if self.approximator_type == 'simplified':
            self.approx_str = f"{self.approximator_type}.{self.approximation_parametrisation}"
        else:
            self.approx_str = f"{self.approximator_type}"

# Factory task to build the approximator
class ApproximatorFactory(ApproximateBase):
    @staticmethod
    def create(approximator_type="simplified", approximation_parametrisation="STXS", *args, **kwargs):
        # Get approximator config
        try:
            approximator = approximator_types[approximator_type]
        except KeyError:
            raise KeyError(f"Approximator type {approximator_type} not found in {approximator_types.keys()}")

        # Construct the task
        if approximator == BuildInterpolated:
            return BuildInterpolated(*args, **kwargs)
        elif approximator == BuildSimplified:
            t = BuildSimplified(*args, **dict(kwargs, parametrisation=approximation_parametrisation))
            return t

class BuildApproximator(law.WrapperTask, ApproximatorFactory, ApproximateBase):
    def requires(self):
        return self.approximator.req(self.approximator)

# TODO merge single and pair?
# TODO base interpolator task?
class ProfileSingle(POITask, ApproximateBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self.pois_split) == 1, f"InterpolateSingle only supports single POIs, not {self.pois_split}"
        self.poi = self.pois_split[0]
        
    def complete(self):
        print("checking complete")
        return super().complete()
    
    def requires(self):
        return BuildApproximator.req(self)

    def output(self):
        return {
            'limits' : self.local_target(f"singles.{self.approx_str}.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{self.poi}.json"),
            'profile' : self.local_target(f"profile.{self.approx_str}.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{self.poi}.npy")
        }
    
    def run(self):    
        # Load the interpolator
        interp = self.input()
        assert isinstance(interp, law.LocalFileTarget)
        with open(interp.path, 'rb') as f:
            interp = pickle.load(f)
        
        # Profile the interpolator
        res = profile1D(interp, self.poi, num=100) # TODO parametrise
        
        # Re-minimise the results
        x_vals = res[self.poi]
        y_vals = 2*(res['deltaNLL'] - res['best'])
        
        # Save the profile
        np.save(self.output()['profile'].path, np.array([x_vals, y_vals]))
        
        # Fit the profiled points
        fit = np.polyfit(x_vals, y_vals, 20)
        
        # Find the 1 and 2 sigma confidence intervals
        ci_1 = np.roots(np.polyadd(fit, [-1]))
        ci_2 = np.roots(np.polyadd(fit, [-4]))
        ci_1 = ci_1[np.isreal(ci_1)].real
        ci_2 = ci_2[np.isreal(ci_2)].real
        
        # Filter to select roots within the bounds
        ci_1 = [c for c in ci_1 if c > min(x_vals) and c < max(x_vals)]
        ci_2 = [c for c in ci_2 if c > min(x_vals) and c < max(x_vals)]
        
        # Get errors
        err_1sig = ci_1 - res['best_x']
        err_2sig = ci_2 - res['best_x']
        
        # Save results to json
        results_dict = {self.model : {self.poi: {}}}
        results_dict[self.model][self.poi]['2sig_ErrorHi'] = max(err_2sig)
        results_dict[self.model][self.poi]['2sig_ErrorLo'] = min(err_2sig)
        results_dict[self.model][self.poi]['ErrorHi'] = max(err_1sig)
        results_dict[self.model][self.poi]['ErrorLo'] = min(err_1sig)
        results_dict[self.model][self.poi]['Val'] = res['best_x']
        with open(self.output()['limits'].path, 'w') as f:
            json.dump(results_dict, f, indent=4)

class ProfilePair(POITask, ApproximateBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self.pois_split) == 2, f"InterpolatePair only supports pairs of POIs, not {self.pois_split}"
        self.pair = self.pois_split
    
    def requires(self):
        return BuildApproximator.req(self)

    def output(self):
        return {
            'profile' : self.local_target(f"profile.{self.approx_str}.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{'_'.join(self.pair)}.npy")
        }
    
    def run(self):    
        # Load the interpolator
        interp = self.input()
        assert isinstance(interp, law.LocalFileTarget)
        with open(interp.path, 'rb') as f:
            interp = pickle.load(f)
        
        # Profile the interpolator
        res = profile2D(interp, self.pair, num=100) # TODO parametrise
        
        # Re-minimise the results
        x_vals = res[self.pair[0]]
        y_vals = res[self.pair[1]]
        z_vals = 2*(res['deltaNLL'] - res['best'])

        # Save the profile
        np.save(self.output()['profile'].path, np.array([x_vals, y_vals, z_vals]))

# TODO merge pairs and singles  
class ProfileSingles(POITask, ScanMethod, ApproximateBase):
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
    
    def requires(self):
        return {poi: ProfileSingle.req(self, pois=poi) for poi in self.pois_split}
    
    def output(self):
        return {
            'limits' : self.local_target(f"singles.{self.approx_str}.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.json"),
            'profiles' : {
                poi: self.local_target(f"profile.{self.approx_str}.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{poi}.npy") for poi in self.pois_split
            }
        }
    
    def run(self):
        # TODO make sure .path is picked up
        # Merge the limits
        results = {poi: self.input()[poi]['limits'] for poi in self.pois_split}
        results_dict = {self.model: {}}
        for poi, result in results.items():
            assert isinstance(result, law.LocalFileTarget)
            with open(result.path, 'r') as f:
                results_dict[self.model][poi] = json.load(f)[self.model][poi]
        with open(self.output()['limits'].path, 'w') as f:
            json.dump(results_dict, f, indent=4)
        
        # Merge the profiles
        profiles = {poi: self.input()[poi]['profile'] for poi in self.pois_split}
        for poi, profile in profiles.items():
            assert isinstance(profile, law.LocalFileTarget)
            with open(profile.path, 'rb') as f:
                profile = np.load(f)
            np.save(self.output()['profiles'][poi].path, profile)
  
class ProfilePairs(POITask, ScanMethod, ApproximateBase):
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
        # Compute pairs
        self.poi_pairs = list(map(','.join, list(combinations(self.pois_split, 2))))
    
    def requires(self):
        return {pair: ProfilePair.req(self, pois=pair) for pair in self.poi_pairs}

    def output(self):
        return {
            'profiles' : {
                pair: self.local_target(f"profile.{self.approx_str}.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{'_'.join(pair.split(','))}.npy") for pair in self.poi_pairs
            }
        }
    
    def run(self):
        # Merge the profiles
        profiles = {pair: self.input()[pair]['profile'] for pair in self.poi_pairs}
        for pair, profile in profiles.items():
            assert isinstance(profile, law.LocalFileTarget)
            with open(profile.path, 'rb') as f:
                profile = np.load(f)
            np.save(self.output()['profiles'][pair].path, profile)            
