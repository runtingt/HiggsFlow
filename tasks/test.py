import law
from io import TextIOWrapper
from tasks.base import BaseTask, ForceableTask, ForceNewerOutputTask, ForceableWithNewer
from termcolor import colored

class TestInputs(law.ExternalTask, BaseTask):
    def output(self):
        return self.local_target("test.txt")

# Create a test task
class Test(ForceableWithNewer, BaseTask):
    """
    Convert a text file and an input file to a RooWorkspace.
    """
    
    def requires(self):
        return TestInputs.req(self)
    
    def output(self) -> law.LocalFileTarget:
        return self.local_target("test_proc.txt")
    
    def run(self) -> None:
        with open(self.output().path, "w") as f:
            assert isinstance(f, TextIOWrapper)
            f.write("Hello, world!")
