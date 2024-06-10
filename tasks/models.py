import luigi
import json
from tasks.combine import ScanAll, ScanPairs, ScanSingles
from tasks.approximation import BuildApproximator, ProfileSingles, ProfilePairs
from tasks.base import ForceableWithNewer
from tasks.utils import ScanMethod, GenericWrapper

class Model():
    def __init__(self, channel: str, model: str, scan_method: str, 
                 type_string: str, attribute_string: str,
                 Scan1D: ScanMethod, Scan2D: ScanMethod,
                 TruthND: ScanMethod, ScanNDEval: ScanMethod,
                 approx_opts: dict=None):
        self.channel = channel
        self.model = model
        self.scan_method = scan_method
        self.types = type_string
        self.attributes = attribute_string
        self.approx_opts = approx_opts
        
        if self.approx_opts is not None:
            self.scan_opts = self.to_params() | self.approx_opts
        else:
            self.scan_opts = self.to_params()
        self.Scan1D = GenericWrapper(task_class=Scan1D(**self.scan_opts))
        self.Scan2D = GenericWrapper(task_class=Scan2D(**self.scan_opts))
        self.TruthND = GenericWrapper(task_class=TruthND(**self.to_params()))
        self.ScanNDEval = GenericWrapper(task_class=ScanNDEval(**self.scan_opts))
        
    def to_params(self):
        params = {
            "channel": self.channel,
            "model": self.model,
            "scan_method": self.scan_method,
            "types": self.types,
            "attributes": self.attributes,
        }
        return params

    def get_reqs(self):
        return {'1D' : self.Scan1D.requires(),
                '2D' : self.Scan2D.requires(),
                'TruthND' : self.TruthND.requires(), # Returns the raw, underlying truth dataset
                'NDEval' : self.ScanNDEval.requires(), # Returns an object with a .evaluate() method
                }

class BuildModel(ForceableWithNewer):
    model_name = luigi.Parameter(
        description="The model to use as the 'truth' dataset. Must be a " \
            "key defined in models_dict."
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.model = models_dict[self.model_name]
        except KeyError:
            raise KeyError(f"Model {self.model_name} not found in {models_dict.keys()}")
        
    def requires(self):
        return self.model.get_reqs()
    
    def output(self):
        return self.local_target(f"{self.model_name}.json")
    
    def run(self):
        with open(self.output().path, 'w') as f:
            json.dump(self.model.to_params(), f, indent=4)
 
# TODO remove unnecessary scans
# TODO add law autocomplete?
models_dict = {
    'hgg_statonly2D_grid_truth':
        Model(channel='hgg_statonly', 
              model='STXStoSMEFTExpandedLinearStatOnly', 
              scan_method='grid', 
              type_string='observed', 
              attribute_string='nominal',
              Scan1D=ScanSingles,
              Scan2D=ScanPairs,
              TruthND=ScanAll,
              ScanNDEval=ScanAll,
              ),
    'hgg_statonly2D_rand_truth':
        Model(channel='hgg_statonly', 
              model='STXStoSMEFTExpandedLinearStatOnly', 
              scan_method='rand', 
              type_string='observed', 
              attribute_string='nominal',
              Scan1D=ScanSingles,
              Scan2D=ScanPairs,
              TruthND=ScanAll,
              ScanNDEval=ScanAll,
              ),
    'hgg_statonly2D_grid_interp':
        Model(channel='hgg_statonly', 
              model='STXStoSMEFTExpandedLinearStatOnly', 
              scan_method='grid', 
              type_string='observed', 
              attribute_string='nominal',
              approx_opts={
                  'approximator_type': 'interpolated',
                  },
              Scan1D=ProfileSingles,
              Scan2D=ProfilePairs,
              TruthND=ScanAll,
              ScanNDEval=BuildApproximator,
              ),
    'hgg_statonly2D_STXS':
        Model(channel='hgg_statonly',
              model='STXStoSMEFTExpandedLinearStatOnly',
              scan_method='grid',
              type_string='observed',
              attribute_string='nominal',
              approx_opts={
                  'approximator_type': 'simplified',
                  'approximation_parametrisation': 'STXS'
                  },
              Scan1D=ProfileSingles,
              Scan2D=ProfilePairs,
              TruthND=ScanAll,
              ScanNDEval=BuildApproximator,
              ),
    'hgg_statonly2D_SMEFT':
        Model(channel='hgg_statonly',
              model='STXStoSMEFTExpandedLinearStatOnly',
              scan_method='grid',
              type_string='observed',
              attribute_string='nominal',
              approx_opts={
                  'approximator_type': 'simplified',
                  'approximation_parametrisation': 'SMEFT'
                  },
              Scan1D=ProfileSingles,
              Scan2D=ProfilePairs,
              TruthND=ScanAll,
              ScanNDEval=BuildApproximator,
              ),
    }
