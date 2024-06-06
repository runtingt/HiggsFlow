import law
import pickle
import numpy as np
import json
from itertools import combinations
from tasks.combine import CombineBase, POITask, ScanAll
from tasks.utils import ScanMethod
from interpolator.base import rbfInterpolator
from interpolator.utils import Data
from interpolator.profiler import profile1D, profile2D
from law.logger import get_logger
logger = get_logger('luigi-interface')

class BuildInterpolator(CombineBase):
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

# TODO merge single and pair?
# TODO base interpolator task?
class InterpolateSingle(POITask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self.pois_split) == 1, f"InterpolateSingle only supports single POIs, not {self.pois_split}"
        self.poi = self.pois_split[0]
    
    def requires(self):
        return BuildInterpolator.req(self)

    def output(self):
        return {
            'limits' : self.local_target(f"singles.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{self.poi}.json"),
            'profile' : self.local_target(f"profile.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{self.poi}.npy")
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

class InterpolatePair(POITask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self.pois_split) == 2, f"InterpolatePair only supports pairs of POIs, not {self.pois_split}"
        self.pair = self.pois_split
    
    def requires(self):
        return BuildInterpolator.req(self)

    def output(self):
        return {
            'profile' : self.local_target(f"profile.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{'_'.join(self.pair)}.npy")
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
class ProfileInterpolated1D(POITask, ScanMethod):
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
    
    def requires(self):
        return {poi: InterpolateSingle.req(self, pois=poi) for poi in self.pois_split}
    
    def output(self):
        return {
            'limits' : self.local_target(f"singles.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.json"),
            'profiles' : {
                poi: self.local_target(f"profile.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{poi}.npy") for poi in self.pois_split
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
  
class ProfileInterpolated2D(POITask, ScanMethod):
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
        # Compute pairs
        self.poi_pairs = list(map(','.join, list(combinations(self.pois_split, 2))))
    
    def requires(self):
        return {pair: InterpolatePair.req(self, pois=pair) for pair in self.poi_pairs}

    def output(self):
        return {
            'profiles' : {
                pair: self.local_target(f"profile.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{'_'.join(pair.split(','))}.npy") for pair in self.poi_pairs
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
