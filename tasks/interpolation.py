import law
import pickle
from tasks.combine import CombineBase, ScanAll
from interpolator.base import rbfInterpolator
from interpolator.utils import Data
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
