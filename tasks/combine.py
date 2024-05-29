import os
import re
import law
import luigi
import shutil
import numpy as np
from typing import Dict
from getPOIs import GetWsp, GetT2WOpts, GetMinimizerOpts, GetPOIsList, SetSMVals, GetPOIRanges, GetFreezeList, GetGeneratePOIs
from tasks.base import BaseTask, ForceableWithNewer
from tasks.remote import HTCondorCPU

from law.logger import get_logger
logger = get_logger('luigi-interface')

# TODO tidy this
# Combine tasks:
# Ensure cmssetup has been run
# Ensure combine is installed
# Be able to parse: command, datacard, method, channel, model, types, attributes, pois (this should be extensible - use a dictionary and a template)
# Return the command that should be run

# The derived classes then actually run the command

class CombineBase(ForceableWithNewer):
    # Define common parameters
    MH = luigi.FloatParameter(
        default="125.38",
        description="nominal Higgs mass; default is 125.38 (GeV)"
    )
    
    channel = luigi.Parameter(
        default="hgg_statonly",
        description="channel to use for the combination; default is hgg_statonly"
    )

    inputs = luigi.Parameter(
        default="comb_2021_hgg.inputs.root",
        description="the name of the root inputs file; default is comb_2021_hgg.inputs.root"
    )
    
    model = luigi.Parameter(
        default="STXStoSMEFTExpandedLinearStatOnly",
        description="model to use for the combination; default is STXStoSMEFTExpandedLinearStatOnly"
    )
    
    # TODO handle multiple types and attributes
    types = luigi.Parameter(
        default="observed",
        description="type of scan to run; default is observed" # TODO change this to something sensible
    )
    
    attributes = luigi.Parameter(
        default="nominal",
        description="attributes of the scan to run; default is nominal"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Look for CMS_PATH in the environment
        self.cms_path = os.getenv("CMS_PATH")
        if self.cms_path is None:
            raise ValueError("CMS_PATH is not set. Please run a cms setup script.")
        
        # Check if CMSSW_BASE is set, and source it if not
        self.cmssw_base = os.getenv("CMSSW_BASE")
        if self.cmssw_base is None:
            raise ValueError("CMSSW_BASE is not set, please run 'cmsenv'")

        # Check if combine is installed
        self.combine_path = shutil.which("combine")
        if self.combine_path is None:
            raise ValueError(f"Combine is not installed in {self.cmssw_base}.")
        else:
            logger.debug(f"Found combine at {self.combine_path}")
        
        # Define frequently used commands
        self.base_command = f"cd {os.environ['CMSSW_PATH']}; cmsenv; cd {os.environ['ANALYSIS_PATH']}; ulimit -s unlimited; "
        self.time_command = "/usr/bin/time -v"
        
        # Parse the model
        self.COMBINE_OPTIONS = GetMinimizerOpts(self.model)
        self.COMBINE_SET_OPTIONS = ""
        self.COMBINE_POIS = GetPOIsList(self.model)
        self.COMBINE_POIS_TO_RUN = GetGeneratePOIs(self.model)
        self.COMBINE_RANGES = GetPOIRanges(self.model)
        self.COMBINE_FREEZE = GetFreezeList(self.model)
        if self.COMBINE_FREEZE != '':
            self.COMBINE_FREEZE = ',' + self.COMBINE_FREEZE
        
    def run_cmd(self, cmd: str) -> None:
        logger.info(f"Running command: {cmd}")
        os.system(cmd)
    
class InputFiles(law.ExternalTask, CombineBase):
    """
    Wrapper for the datacard and inputs files that are needed to run
    the combination.
    """
    
    def output(self) -> Dict[str, law.LocalFileTarget]:
        datacard = self.local_target(f"comb_2021_{self.channel}.txt.gz")
        roo_inputs = self.local_target(self.inputs)
        files = {"datacard": datacard, "roo_inputs": roo_inputs}
        return files
    
class TextToWorkspace(CombineBase):
    """
    Convert a text file and an input file to a RooWorkspace.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def requires(self) -> law.Task:
        return InputFiles.req(self) # Pass args through
    
    def output(self) -> law.LocalFileTarget:
        # Get the workspace name from the model
        self.wsp_name = GetWsp(self.model)
        self.wsp_opts = GetT2WOpts(self.model)
        
        # Fix to add full file path to mergejson for STXS fits
        if "mergejson" in self.wsp_opts:
            self.wsp_opts = re.sub("mergejson=", f"mergejson={os.environ['ANALYSIS_PATH']}/", self.wsp_opts)

        # Build wsp file
        self.wsp_file = f"ws_{self.channel}_{self.wsp_name}"
        return {'workspace': self.local_target(f"{self.wsp_file}_attr.root"), 
                'log': self.local_target(f"t2w_{self.channel}_{self.model}_local.log")}
    
    def run(self) -> None:
        outdir = self.local_path()
        card_target = self.input()["datacard"]
        assert isinstance(card_target, law.LocalFileTarget)
        card_path = card_target.path
        logger.info(f"Running: TextToWorkspace, will output {self.output()}")

        wsp_target = self.output()['workspace']
        assert isinstance(wsp_target, law.LocalFileTarget) 
        # Build and run the command
        cmd = self.base_command
        cmd += (
            f"{self.time_command} text2workspace.py -o {wsp_target.basename} {card_path} {self.wsp_opts}"
            f" &> {outdir}/t2w_{self.channel}_{self.model}_local.log;"
            f" mv {wsp_target.basename} {wsp_target.path}"
        )
        self.run_cmd(cmd)

class InitialFit(CombineBase, HTCondorCPU, law.LocalWorkflow):    
    def create_branch_map(self):
        return [None] # Single branch, no special data
    
    def workflow_requires(self):
        return []
    
    def requires(self):
        return TextToWorkspace.req(self)
    
    def output(self):
        return {'tree': self.local_target(f"higgsCombine.initial.{self.channel}.{self.model}.{self.types}.MultiDimFit.mH{self.MH}.123456.root"),
                'log': self.local_target(f"initialfit_{self.channel}_{self.model}_local.log")}
    
    def run(self):        
        logger.info(f"Running: InitialFit, will output {self.output()}")
        
        # Build generate string
        GENERATE_STR = "n;t;toysFrequentist;"
        if 'observed' in self.types: GENERATE_STR += ";observed,!,!"
        if 'prefit_asimov' in self.types: GENERATE_STR += ";prefit_asimov,-1,!"
        if 'postfit_asimov' in self.types: GENERATE_STR += ";postfit_asimov,-1, "
        input = self.input()
        assert isinstance(input, law.LocalFileTarget)
        ws_path = input.path

        # Build and run the command
        cmd = self.base_command
        cmd += (
            f"{self.time_command} combineTool.py -M MultiDimFit "
            f"-m {self.MH} -d {ws_path} "
            f"--redefineSignalPOIs {self.COMBINE_POIS} --setParameters {self.COMBINE_SET} "
            f"--setParameterRanges {self.COMBINE_RANGES} --freezeParameters MH{self.COMBINE_FREEZE} "
            f"--generate '{GENERATE_STR}' --saveToys --saveWorkspace {self.COMBINE_OPTIONS} "
            f"-n .initial.{self.channel}.{self.model} "
            f"&> {self.output()['tree'].dirname}/initialfit_{self.channel}_{self.model}_local.log;"
        )
        cmd += f"mv {self.output()['tree'].basename} {self.output()['tree'].path};"
        self.run_cmd(cmd)

# TODO refactor so that only the base class is here. We will define all the scans (and the factory) in a separate file
class ScanBase(CombineBase, HTCondorCPU, law.LocalWorkflow):
    """
    Base class for running a scan
    """
    n_points = luigi.IntParameter(
        default=10,
        description="number of points to run; default is 10"
    )
    
    points_per_job = luigi.IntParameter(
        default=1,
        description="number of points to run per job; default is 1"
    )

    scan_method = luigi.Parameter(
        default="grid",
        description="scan method to use; default is grid"
    )
    
    def create_branch_map(self):
        return {i: i for i in range(int(np.ceil(self.n_points / self.points_per_job)))}
    
    def workflow_requires(self):
        return {'init': InitialFit.req(self)} # No unique requirements per-branch
    
    def requires(self):
        return None # No unique requirements per-branch
    
class ScanPOIBase(ScanBase):
    """
    Base class for running a single-POI scan
    """
    poi = luigi.Parameter(
        default="r",
        description="parameter of interest to scan; default is r"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.start = self.branch * self.points_per_job
        self.end = min(self.start + (self.points_per_job-1), self.n_points)
        
    def output(self):
        return self.local_target(f"higgsCombine.scan.{self.channel}.{self.model}.{self.scan_method}.{self.poi}.POINTS.{self.start}.{self.end}.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root")
        
class ScanPOIGrid(ScanPOIBase):
    """
    Derived class for scanning a single poi using a grid
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **dict(kwargs, scan_method="grid"))
        
    def run(self):
        logger.info(f"Running: ScanPOIGrid for {self.poi}, will output {self.output()}")        
        initial_fit_target = self.input()['tree']
        assert isinstance(initial_fit_target, law.LocalFileTarget)
        initial_path = initial_fit_target.path

        # Build strings
        # TODO offload to parent class
        SKIP_OPTIONS = "--skipInitialFit"
        
        GENERATE_STR = "d;D;n;"
        if 'observed' in self.types: GENERATE_STR += f";{initial_path},data_obs,observed"
        if 'prefit_asimov' in self.types: GENERATE_STR += f";{initial_path},toys/toy_asimov,prefit_asimov"
        if 'postfit_asimov' in self.types: GENERATE_STR += f";{initial_path},toys/toy_asimov,postfit_asimov"
        
        ATTRIBUTES_STR = "freezeWithAttributes;n;"
        if "nominal" in self.attributes: ATTRIBUTES_STR += ";,nominal"
        if "fr.all" in self.attributes: ATTRIBUTES_STR += ";all,fr.all"
        if "fr.sigth" in self.attributes: ATTRIBUTES_STR += ";sigTheory,fr.sigth"
        if "fr.sigbkgth" in self.attributes: 
            # Requires doubling of commas to account for two frozen attributes
            ATTRIBUTES_STR = re.sub(",", ",,", ATTRIBUTES_STR)
            ATTRIBUTES_STR += ";sigTheory,bkgTheory,,fr.sigbkgth"

        # TODO offload to parent class
        cmd = self.base_command
        cmd += (
            f" {self.time_command} combineTool.py -M MultiDimFit -m {self.MH}"
            f" --generate \"{GENERATE_STR}\" \"{ATTRIBUTES_STR}\""# \"{self.COMBINE_POIS_TO_RUN}\""
            f" --freezeParameters MH{self.COMBINE_FREEZE} --redefineSignalPOIs {self.COMBINE_POIS}"
            f" --setParameterRanges {self.COMBINE_RANGES} {self.COMBINE_OPTIONS}"
            f" -n .scan.{self.channel}.{self.model}.{self.scan_method}.{self.poi}.POINTS.{self.start}.{self.end}"
            f" --snapshotName \"MultiDimFit\" --algo grid --saveInactivePOI 1"
            f" {SKIP_OPTIONS} {self.COMBINE_SET_OPTIONS}"
            f" --points {self.n_points} --alignEdges 1 -P {self.poi}"
            f" --firstPoint {self.start} --lastPoint {self.end}"
            f"&> {self.output().dirname}/scan_{self.channel}_{self.model}_{self.poi}_local.log;"
        )
        cmd += f"mv {self.output().basename} {self.output().path}"
        self.run_cmd(cmd)

class ScanPOI(ScanPOIGrid):
    """
    Factory class for creating scan tasks
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scan_classes = {
            'grid': ScanPOIGrid
            # TODO add scan from file that supports reading in from a file (which can be specified in a similar way to the factory)
        }
        self.create_scan(*args, **kwargs)
    
    def create_scan(self, *args, **kwargs):
        scan_class = self._scan_classes.get(self.scan_method)
        if scan_class is None:
            raise ValueError(f"Scan method {self.scan_method} not recognised.")
        self.scan = scan_class(*args, **kwargs)
    
    def run(self):
        self.scan.run()
    
