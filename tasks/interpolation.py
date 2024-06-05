import law
import pickle
import numpy as np
import json
from tasks.combine import CombineBase, POITask, ScanAll
from interpolator.base import rbfInterpolator
from interpolator.utils import Data
from interpolator.profiler import profile1D
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

class InterpolateSingle(POITask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert len(self.pois_split) == 1, f"InterpolateSingle only supports single POIs, not {self.pois_split}"
        self.poi = self.pois_split[0]
    
    def requires(self):
        return BuildInterpolator.req(self)

    def output(self):
        return self.local_target(f"singles.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.{self.poi}.json")
    
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
        with open(self.output().path, 'w') as f:
            json.dump(results_dict, f, indent=4)
        
class InterpolateSingles(POITask):
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
    
    def requires(self):
        return [InterpolateSingle.req(self, pois=poi) for poi in self.pois_split]
    
    def output(self):
        return self.local_target(f"singles.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.json")
    
    def run(self):
        # Merge the results
        results = {poi: self.input()[i] for i, poi in enumerate(self.pois_split)}
        results_dict = {self.model: {}}
        for poi, result in results.items():
            assert isinstance(result, law.LocalFileTarget)
            with open(result.path, 'r') as f:
                results_dict[self.model][poi] = json.load(f)[self.model][poi]
        with open(self.output().path, 'w') as f:
            json.dump(results_dict, f, indent=4)
