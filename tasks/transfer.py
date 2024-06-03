import law
import os
from io import TextIOWrapper
from tasks.combine import CombineBase, ScanSingles, ScanPairs

class TransferOut(CombineBase):
    """
    Transfer outputs to a remote location (eos) using `rsync`
    """
    
    def requires(self):
        return {'singles': ScanSingles.req(self), 'pairs': ScanPairs.req(self)}
    
    def output(self):
        # TODO use wlcg
        return law.LocalFileTarget(self.local_path("output.txt"))
    
    def run(self):
        # with open(self.output().path, 'w') as f:
            # assert isinstance(f, TextIOWrapper)
            # f.write("Hello, World!")

        # Transfer the output files of the dependencies to eos
        # TODO remove hardcoding
        to_transfer = os.path.join(os.getenv('DATA_PATH'), 'PlotPOIs')
        cmd = f"kswitch -p {os.getenv('EOS_KERBEROS')}; "
        cmd += f'xrdcp -r -f {to_transfer} root://eosuser.cern.ch/{os.getenv("EOS_PATH")}; '
        cmd += f"kswitch -p {os.getenv('USER')}"
        self.run_cmd(cmd)
