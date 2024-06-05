import os
import law
import law.util
import law.contrib
import law.contrib.htcondor
from tasks.base import BaseTask

law.contrib.load("htcondor")

class BaseRemote(law.htcondor.HTCondorWorkflow, BaseTask):
    """
    Base workflow that allows submission to htcondor
    """
    
    max_runtime = law.DurationParameter(
        default=1.0,
        unit="hours",
        significant=False,
        description="maximum runtime; default unit is hours; default is 1.0",
    )
    transfer_logs = law.OptionalBoolParameter(
        default=True,
        significant=False,
        description="transfer log files to the output dir; default is True",
    )
    
    def htcondor_output_directory(self) -> law.LocalDirectoryTarget:
        """
        Defines the directory where submission data will be stored
        """
        return law.LocalDirectoryTarget(self.local_path())
    
    def htcondor_bootstrap_file(self) -> law.JobInputFile:
        """
        Defines the boostrap file that is executed prior to the actual job,
        shared across jobs and rendered as part of the job itself
        """
        bootstrap_file = law.util.rel_path(__file__, "bootstrap.sh")
        return law.JobInputFile(bootstrap_file, share=True, render_job=True)

class HTCondorCPU(BaseRemote):
    """
    CPU job submission to htcondor
    """
    def htcondor_job_config(self, config, job_num, branches):
        # Render variables are rendered into all files sent to a job
        config.render_variables["analysis_path"] = os.getenv("ANALYSIS_PATH")
        
        # Target el9
        # config.custom_content.append(("requirements", '(OpSysAndVer =?= "AlmaLinux9")'))
        
        # Set max runtime from variable
        config.custom_content.append(("+MaxRuntime", int(self.max_runtime * 3600)))
        
        # Copy environment variables
        # TODO bundle CMSSW instead
        config.custom_content.append(("getenv", "true"))
        
        # Ignore the logs
        # TODO reverse this
        config.custom_content.append(("log", "/dev/null"))
        
        return config
    
class HTCondorGPU(BaseRemote):
    """
    GPU job submission to htcondor
    """

    def htcondor_job_config(self, config, job_num, branches):
        # Render variables are rendered into all files sent to a job
        config.render_variables["analysis_path"] = os.getenv("ANALYSIS_PATH")
        
        # Target el9
        # config.custom_content.append(("requirements", '(OpSysAndVer =?= "AlmaLinux9")'))
        
        # Set max runtime from variable
        config.custom_content.append(("+MaxRuntime", int(self.max_runtime * 3600)))
    
        # Request a GPU
        config.custom_content.append(("request_gpus", 1))
        
        # Copy environment variables
        # TODO bundle CMSSW instead
        config.custom_content.append(("getenv", "true"))
        
        # Ignore the logs
        # TODO reverse this
        config.custom_content.append(("log", "/dev/null"))
        
        return config
