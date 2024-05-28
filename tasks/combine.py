import os
import re
import law
import luigi
import shutil
import subprocess
from typing import Dict
from getPOIs import GetWsp, GetT2WOpts
from tasks.base import BaseTask, ForceableWithNewer

from law.logger import get_logger
logger = get_logger('luigi-interface')

# Combine tasks:
# Ensure cmssetup has been run
# Ensure combine is installed
# Be able to parse: command, datacard, method, channel, model, types, attributes, pois (this should be extensible - use a dictionary and a template)
# Return the command that should be run

# The derived classes then actually run the command


def source_and_get_environment(script, shell="/bin/bash"):
    command = [shell, "-c", f"{script} && env"]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in proc.stdout:
        line = line.decode()
        (key, _, value) = line.partition("=")
        os.environ[key] = value.strip()
    proc.communicate()

class CombineBase(BaseTask):
    # Define common parameters
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Look for CMS_PATH in the environment
        self.cms_path = os.getenv("CMS_PATH")
        if self.cms_path is None:
            raise ValueError("CMS_PATH is not set. Please run a cms setup script.")
        
        # Check if CMSSW_BASE is set, and source it if not
        self.cmssw_base = os.getenv("CMSSW_BASE")
        if self.cmssw_base is None:
            logger.info("CMSSW_BASE is not set. Attempting to use $CMSSW_PATH from setup script.")
            cmd = f"cd {os.environ['CMSSW_PATH']};"
            cmd += "cmsenv;"
            cmd += f"cd {os.environ['ANALYSIS_PATH']}"
            source_and_get_environment(cmd)
            logger.info(f"CMSSW_BASE is now set to {os.getenv('CMSSW_BASE')}")
        self.cmssw_base = os.getenv("CMSSW_BASE")
        if self.cmssw_base is None:
            raise ValueError("CMSSW_BASE could not be set.")

        # Check if combine is installed
        self.combine_path = shutil.which("combine")
        if self.combine_path is None:
            raise ValueError(f"Combine is not installed in {self.cmssw_base}.")
        
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

        # Don't run if workspace already exists
        wsp_target = self.output()['workspace']
        assert isinstance(wsp_target, law.LocalFileTarget) 
        if os.path.exists(wsp_target.path) and not self.force:
            logger.info(f"Workspace already exists for channel [{self.channel}], model [{self.model}]")
        else:
            # Build and run the command
            cmd = self.base_command
            cmd += (
                f"{self.time_command} text2workspace.py -o {wsp_target.basename} {card_path} {self.wsp_opts}"
                f" &> {outdir}/t2w_{self.channel}_{self.model}_local.log;"
                f" mv {wsp_target.basename} {wsp_target.path}"
            )
            self.run_cmd(cmd)
            