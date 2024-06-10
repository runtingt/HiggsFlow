import os
import law
import law.target
import luigi
import numpy as np
from typing import Dict, List, Tuple, Union
from law.task.base import BaseTask as LawBaseTask # For proper type-hinting
from law.target.base import Target
from law.logger import get_logger

logger = get_logger('luigi-interface')

# Get a list of targets from a dict, list, tuple, or single target
def targetAsList(target: Union[Dict, List, Tuple, law.LocalFileTarget]) -> List[law.LocalFileTarget]:
    if isinstance(target, dict):
        return list(target.values())
    elif isinstance(target, (list, tuple)):
        return target
    elif isinstance(target, law.LocalFileTarget):
        return [target]
    else:
        raise ValueError(f"Invalid target type: {type(target)}")

def flatten(collection):
    result = []
    for i in collection:
        if isinstance(i, law.TargetCollection):
            result.extend(flatten(i.targets))
        else:
            if isinstance(i, Union[Dict, List, Tuple]):
                result.extend(flatten(targetAsList(i)))
            elif isinstance(i, Target):
                result.append(i)
    return result

# Get the last modification time of a target
def getTargetModificationTime(target: law.LocalFileTarget) -> float:
    return os.path.getmtime(target.path)

class BaseTask(law.Task, LawBaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create the output directory if it doesn't exist
        expanded_path = os.path.expandvars(self.local_path())
        logger.debug(f"Attempting to create directory {expanded_path}")
        os.makedirs(expanded_path, exist_ok=True)

    # Helper methods for defining local paths and targets 
    def local_path(self, *path) -> str:        
        # $DATA_PATH is set in setup.sh
        parts = (os.getenv("DATA_PATH"),) + (self.__class__.__name__,) + path
        return os.path.join(*parts)
    def local_target(self, *path) -> law.LocalFileTarget:
        return law.LocalFileTarget(self.local_path(*path))
    
# Define a task that adds forceability to the base class
class ForceableTask(BaseTask):
    force = luigi.BoolParameter(default=False, description="Force the task to run. Default is False.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_run = False
    
    def run(self): # NOTE: This must be called by the derived class
        self.has_run = True
        # print('ForceableTask run method was called')
    
    def complete(self):
        if self.force and not self.has_run:
            logger.debug(f"Forcing task {self.__class__.__name__} to run")
            return False
        else:
            return BaseTask.complete(self)

# Define a task that forces the outputs to be newer than the inputs
# TODO make this traverse the entire tree, not just the level below
class ForceNewerOutputTask(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def complete(self):
        # Check if the outputs are newer than the inputs
        inputs = self.input()
        
        # Get outputs if the output method is defined
        if hasattr(self, "output"):
            outputs = self.output()
        else:
            outputs = []
        
        # Get targets as lists
        inputs_list = targetAsList(inputs)
        outputs_list = targetAsList(outputs)
        
        # Expand any target collections
        inputs_list_expanded = []
        outputs_list_expanded = []
        for item in inputs_list:
            if isinstance(item, law.TargetCollection):
                inputs_list_expanded.append(item.targets)
            else:
                inputs_list_expanded.append(item)
        for item in outputs_list:
            if isinstance(item, law.TargetCollection):
                outputs_list_expanded.append(item.targets)
            else:
                outputs_list_expanded.append(item)
        # Get a flat list of targets
        inputs_list_expanded = flatten([targetAsList(item.targets) if isinstance(item, law.TargetCollection) else item for item in inputs_list])
        outputs_list_expanded = flatten([targetAsList(item.targets) if isinstance(item, law.TargetCollection) else item for item in outputs_list])       
        inputs_list = inputs_list_expanded
        outputs_list = outputs_list_expanded

        # Check if files exist
        inputs_to_check = inputs_list.copy()
        for input in inputs_list:
            if input.optional:
                inputs_to_check.remove(input)
                continue
            if not input.exists():
                logger.debug(f"Task {self.__class__.__name__} is missing input {input}")
                return False # When the now-missing input is created, it will be newer than the outputs
        outputs_to_check = outputs_list.copy()
        for output in outputs_list:
            if output.optional:
                outputs_to_check.remove(output)
                continue
            if not output.exists() and output.optional == False:
                logger.debug(f"Task {self.__class__.__name__} is missing output {output}")
                return False
            
        # The task is complete if all outputs are newer than all inputs
        input_times = [getTargetModificationTime(input) for input in inputs_to_check]
        if len(input_times) == 0:
            return BaseTask.complete(self) 
        newest_idx = np.argmax(input_times)
        newest_input = inputs_list[newest_idx]
        newest_input_time = input_times[newest_idx]
        output_times = [getTargetModificationTime(output) for output in outputs_to_check]
        if len(output_times) == 0:
            return BaseTask.complete(self)
        oldest_idx = np.argmin(output_times)
        oldest_output = outputs_list[oldest_idx]
        oldest_output_time = output_times[oldest_idx]
        
        logger.debug(f"Newest input: {newest_input} @ {newest_input_time}")
        logger.debug(f"Oldest output: {oldest_output} @ {oldest_output_time}")
        
        if newest_input_time > oldest_output_time:
            logger.debug(f"Task {self.__class__.__name__} is incomplete because {newest_input} is more recent than {oldest_output}")
            return False
        else:
            return BaseTask.complete(self)

# Combine forceability and newer-output checking
class ForceableWithNewer(ForceableTask, ForceNewerOutputTask):
    force = luigi.BoolParameter(default=False, description="Force the task to run. Default is False.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def complete(self):
        flag = ForceableTask.complete(self)
        if not flag:
            return False
        else:
            flag = ForceNewerOutputTask.complete(self)
            if not flag:
                logger.debug(f"Task {self.__class__.__name__} is out of date")
            return flag
        
    def run(self):
        super().run() # Call the ForceableTask run method

