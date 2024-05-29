import os
import re
import law
import luigi
import shutil
from typing import Dict
from getPOIs import GetWsp, GetT2WOpts, GetMinimizerOpts, GetPOIsList, SetSMVals, GetPOIRanges, GetFreezeList
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

class CombineBase(BaseTask):
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
    
    types = luigi.Parameter(
        default="observed",
        description="type of scan to run; default is observed" # TODO change this to something sensible
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
    
class TextToWorkspace(CombineBase, ForceableWithNewer):
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

class InitialFit(CombineBase, ForceableWithNewer, HTCondorCPU, law.LocalWorkflow):    
    def create_branch_map(self):
        return [None] # Single branch, no special data
    
    def workflow_requires(self):
        return []
    
    def requires(self):
        return TextToWorkspace.req(self) # No dependencies for the branch, just the workflow itself
    
    def output(self):
        return {'tree': self.local_target(f"higgsCombine.initial.{self.channel}.{self.model}.{self.types}.MultiDimFit.mH.{self.MH}.123456.root"),
                'log': self.local_target(f"initialfit_{self.channel}_{self.model}_local.log;")}
    
    def run(self):        
        logger.info(f"Running: InitialFit, will output {self.output()}")
        channel = self.channel
        model = self.model 
        types = self.types

        # Get options from getPOIs 
        # TODO offload this to base
        COMBINE_OPTIONS = GetMinimizerOpts(model)
        COMBINE_POIS = GetPOIsList(model)
        COMBINE_SET = SetSMVals(model)
        COMBINE_RANGES = GetPOIRanges(model)
        COMBINE_FREEZE = GetFreezeList(model)
        if COMBINE_FREEZE != '':
            COMBINE_FREEZE = ',' + COMBINE_FREEZE
        
        GENERATE_STR = "n;t;toysFrequentist;"
        if 'observed' in types: GENERATE_STR += ";observed,!,!"
        if 'prefit_asimov' in types: GENERATE_STR += ";prefit_asimov,-1,!"
        if 'postfit_asimov' in types: GENERATE_STR += ";postfit_asimov,-1, "
        input = self.input()
        assert isinstance(input, law.LocalFileTarget)
        ws_path = input.path

        # Build and run the command
        cmd = self.base_command
        cmd += (
            f"{self.time_command} combineTool.py -M MultiDimFit "
            f"-m {self.MH} -d {ws_path} "
            f"--redefineSignalPOIs {COMBINE_POIS} --setParameters {COMBINE_SET} "
            f"--setParameterRanges {COMBINE_RANGES} --freezeParameters MH{COMBINE_FREEZE} "
            f"--generate '{GENERATE_STR}' --saveToys --saveWorkspace {COMBINE_OPTIONS} "
            f"-n .initial.{channel}.{model} "
            f"&> {self.output()['tree'].dirname}/initialfit_{channel}_{model}_local.log;"
        )
        cmd += f"mv {self.output()['tree'].basename} {self.output()['tree'].path};"
        self.run_cmd(cmd)
