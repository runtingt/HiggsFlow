import law
import luigi
from law.task.base import BaseTask as LawBaseTask
from tasks.base import ForceableWithNewer

colors = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]
need_pre = ["hgg", "hzz", "hmm", "hbb_boosted_stxs", "hinv"]

def deep_merge(dict1: dict, dict2: dict):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            deep_merge(dict1[key], value)
        else:
            dict1[key] = value
class ScanMethod(ForceableWithNewer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def requires(self):
        raise NotImplementedError("ScanMethod is a base class and should not be used directly")

    def output(self):
        raise NotImplementedError("ScanMethod is a base class and should not be used directly")             

class GenericWrapper(law.WrapperTask):
    task_class = luigi.TaskParameter(description="The task class to wrap")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def requires(self):
        assert isinstance(self.task_class, LawBaseTask)
        return self.task_class.req(self.task_class)
