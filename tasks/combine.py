import os
import re
import law
import law.decorator
import luigi
import shutil
import json
import numpy as np
import uproot
import torch
import pandas as pd
import gpytorch
import glob
from gaussianProcesses.base import GPModel, EarlyStopper, normalise, unnormalise
from io import TextIOWrapper
from typing import Dict
from getPOIs import GetWsp, GetT2WOpts, GetMinimizerOpts, GetPOIsList, GetPOIRanges, GetFreezeList, SetSMVals
from itertools import combinations
from tasks.base import ForceableWithNewer
from tasks.remote import HTCondorCPU, HTCondorGPU
from tasks.notify import NotifySlackParameterUTF8, SplitTimeDecorator
from tasks.utils import deep_merge, need_pre

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
    
    # TODO offer getPOIs as an autocomplete
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
    
    scan_method = luigi.Parameter(
        default="grid",
        description="scan method to use; default is grid"
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
            raise ValueError("CMSSW_BASE is not set, please run 'cmsenv'. Make sure to reactivate this environment after.")

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
        self.COMBINE_SET = SetSMVals(self.model)
        self.COMBINE_SET_OPTIONS = ""
        self.COMBINE_POIS = GetPOIsList(self.model)
        # self.COMBINE_POIS_TO_RUN = GetGeneratePOIs(self.model)
        self.COMBINE_RANGES = GetPOIRanges(self.model)
        self.COMBINE_FREEZE = GetFreezeList(self.model)
        if self.COMBINE_FREEZE != '':
            self.COMBINE_FREEZE = ',' + self.COMBINE_FREEZE
            
        # Get poi bounds
        bound_strs = self.COMBINE_RANGES.split(':')
        bounds = []
        for poi, bound_str in zip(self.COMBINE_POIS.split(','), bound_strs):
            assert poi in bound_str, f"{poi} does not match {bound_strs}"
            lo, hi = map(float, bound_str.split('=')[1].split(','))
            bounds.append(np.array([lo, hi]))
        self.bounds = np.array(bounds)
        
    def run_cmd(self, cmd: str) -> None:
        logger.info(f"Running command: {cmd}")
        os.system(cmd)
        
    def run_cmd_with_base(self, cmd: str) -> None:
        cmd = self.base_command + cmd
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
    
class CloneSingle(CombineBase):
    """
    Clone a single channel from the CADI github area
    """
    def output(self):
        return self.local_target(os.path.join(os.getenv('HC_PATH'), self.channel))
    
    def run(self):
        # TODO tidy the clone_single script itself
        cmd = f"$ANALYSIS_PATH/clone_single.sh ssh clean {self.channel};"
        cmd += f"mv $ANALYSIS_PATH/{self.channel} $HC_PATH"
        self.run_cmd(cmd)
        
class PrePrepare(CombineBase):
    """
    Runs the 'pre' step for a channel
    """
    # TODO make condor workflow
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.channel not in need_pre:
            raise ValueError(f"Channel {self.channel} does not need a pre step, only {need_pre} do") 
    
    def requires(self):
        return CloneSingle.req(self)
    
    def output(self):
        return self.local_target(f"log.{self.channel}.txt")
    
    def run(self):        
        if self.channel == "hgg":
            files = glob.glob("$HC_PATH/hgg/Models/signal/*.root")
            for f in files: 
                self.run_cmd_with_base(f"python3 hggCleanWsp.py -w {f}:wsig_13TeV -o {re.sub('.root', '_cleaned.root', f)} 2>&1 >/dev/null")
            files_cleaned = glob.glob("$HC_PATH/hgg/Models/signal/*_cleaned.root")
            for f in files_cleaned: 
                self.run_cmd_with_base(f"python3 signalMemOpt.py --file {f}")
            files_cleaned_constMH = glob.glob("$HC_PATH/hgg/Models/signal/*constMH.root")       
            for f in files_cleaned_constMH:
                self.run_cmd_with_base(f"python3 workspaceExplorer.py -w {f}:wsig_13TeV --optimize 1 -o {re.sub('_cleaned_constMH.root', 'updated.root', f)} 2>&1 >/dev/null")
            self.run_cmd_with_base("cat $HC_PATH/hgg/Datacard.txt | sed 's/\\\\(signal.*\\\\)\\\\.root/\\\\1_updated.root/g' > $HC_PATH/hgg/DatacardLowMem.txt")
        
        elif self.channel == "hzz":
            for fint in [6,7,8]: # TODO this should be more specific - is it supposed to be by year?
                files = glob.glob(f"$HC_PATH/hzz/stxs_trueBins/legacy/*{fint}.root")
                for f in files:
                    self.run_cmd_with_base(f"python3 signalMemOpt.py --file {f}")
                # TODO should this be files_constMH? 
                # It is in the original script but never used
                for f in files:
                    self.run_cmd_with_base(f"python3 workspaceExplorer.py -w {f}:w --optimize 2 -o {re.sub('.root', '_updated.root', f)}")
            self.run_cmd_with_base("cat $HC_PATH/hzz/stxs_trueBins/legacy/card_run2.txt | sed 's/.root/_constMH_updated.root/g' > $HC_PATH/hzz/stxs_trueBins/legacy/card_run2_hzzLowMem.txt")

        elif self.channel == "hmm":
            self.run_cmd_with_base("python3 hmmCleanWsp.py $HC_PATH/hmm/combination/check_2020_ggh.txt $HC_PATH/hmm/combination/check_2020_ggh125.38.inputs.root")
            
        elif self.channel == "hbb_boosted_stxs":
            self.run_cmd_with_base(f"cd $HC_PATH/hbb_boosted/stxs-stage1-2-fine/testModel/; ./build.sh; cd $ANALYSIS_PATH")
            
        elif self.channel == "hinv":
            for wsp in ["MJ", "MV"]:
                self.run_cmd_with_base(f"python3 hinvFixFormulas.py $HC_PATH/hinv/combination_alltime/exo-20-004/workspace_{wsp}.root")

        with open(self.output().path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            f.write(f"Channel [{self.channel}] has been optimized")
        
class Prepare(CombineBase):
    """
    Runs the 'prepare' step for a given channel
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards_dir = os.path.join(os.getenv("HC_PATH"), "cards")
        os.makedirs(self.cards_dir, exist_ok=True)
    
    def requires(self):
        if self.channel in need_pre:
            return PrePrepare.req(self)
        else:
            return CloneSingle.req(self)
        
    def output(self):
        return {
            'log' : self.local_target(f"log.{self.channel}.txt"),
            'card' : law.LocalFileTarget(f"{self.cards_dir}/comb_2021_{self.channel}.txt.gz"),
            'inputs' : law.LocalFileTarget(f"{self.cards_dir}/comb_2021_{self.channel}.inputs.root"),
        }
    
    def run(self):
        PREPARE_OPTIONS = "--prune-asymm-lnN --drop-procs --replace-mc-stats"
        EXTRA_OPTIONS = ""
        if self.channel in ["hzg", "hinv"]:
            EXTRA_OPTIONS = f" --include{self.channel}"

        cmd = self.base_command
        cmd += "cd $HC_PATH;"
        cmd += (
            f"{self.time_command} python3 $ANALYSIS_PATH/prepareComb2021.py "
            f"{PREPARE_OPTIONS} --select {self.channel} {EXTRA_OPTIONS} "
            f"&> {self.output()['log'].path}; "
        )
        cmd += "cd $ANALYSIS_PATH;"
        self.run_cmd(cmd)

        # Ugly fix for hmm
        if self.channel == "hmm":
            self.run_cmd("gunzip $HC_PATH/comb_2021_hmm.txt.gz")
            self.run_cmd("sed -i'' 's@sm_yr4_13TeV.root:xs_13TeV@&:RecycleConflictNodes@g' $HC_PATH/comb_2021_hmm.txt")
            self.run_cmd("sed -i'' 's@sm_br_yr4.root:br@&:RecycleConflictNodes@g' $HC_PATH/comb_2021_hmm.txt")
            self.run_cmd("gzip $HC_PATH/comb_2021_hmm.txt")

        # Move output of prepare step into the cards directory
        self.run_cmd(f"mv -v $HC_PATH/comb_2021_{self.channel}.txt.gz {self.output()['card'].path}")
        self.run_cmd(f"mv -v $HC_PATH/comb_2021_{self.channel}.inputs.root {self.output()['inputs'].path}")

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
        return {'wsp': TextToWorkspace.req(self)}
    
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
        input = self.input()['workspace']
        assert isinstance(input, law.LocalFileTarget), f"Expected LocalFileTarget, got {input, type(input)}"
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
        
class Impacts(CombineBase, HTCondorCPU, law.LocalWorkflow):
    def create_branch_map(self):
        return [None] # Single branch, no special data
    
    def workflow_requires(self):
        return {'init' : InitialFit.req(self)}
    
    def requires(self):
        return InitialFit.req(self)
    
    def output(self):
        return {
            'robustFit' : self.local_target(f"higgsCombine.robustHesse.{self.channel}.{self.model}.{self.types}.MultiDimFit.mH125.38.root"),
            'hessian' : self.local_target(f"hessian_{self.channel}_{self.model}.{self.types}.root"),
            'robustHesse': self.local_target(f"robustHesse.robustHesse.{self.channel}.{self.model}.{self.types}.root")
        }
    
    def run(self):
        initial_target = self.input()['tree']
        assert isinstance(initial_target, law.LocalFileTarget)
        initial_path = initial_target.path
        dataset = "toys/toy_asimov"
        if self.types == "observed":
            dataset = "data_obs"
        cmd = self.base_command
        # TODO include rgx{prop.*} in the freeze list (this breaks hgg_statonly atm)
        cmd += (
            f"{self.time_command} combineTool.py -M MultiDimFit "
            f"-m {self.MH} -d {initial_path} "
            f"--redefineSignalPOIs {self.COMBINE_POIS} "
            f"--saveInactivePOI 1 --snapshotName MultiDimFit "
            f"--freezeParameters MH{self.COMBINE_FREEZE} "
            f"-D {dataset} {self.COMBINE_OPTIONS} --robustHesse 1 --robustFit 1 "
            f"--robustHesseSave hessian_{self.channel}_{self.model}.{self.types}.root "
            f"-n .robustHesse.{self.channel}.{self.model}.{self.types} -v 3 "
            f"&> {self.output()['robustHesse'].dirname}/impacts_{self.channel}_{self.model}_{self.types}_local.log;"
            )
        for output in self.output().values():
            cmd += f"mv {output.basename} {output.path};"
        self.run_cmd(cmd)            

class POITask(CombineBase):
    """
    Base class for tasks that work with POIs
    """
    pois = luigi.Parameter(
        default="r",
        description="comma-separaterd POIs to scan; default is r"
    )
    
    n_points = luigi.IntParameter(
        default=10,
        description="number of points to run; default is 10"
    )
    
    points_per_job = luigi.IntParameter(
        default=2,
        description="number of points to run per job; default is 2"
    )
    
    points_per_block = luigi.OptionalIntParameter(
        default=None,
        description="number of points to run per block, used for GP scanning; default is None"
    )
    
    block_index = luigi.OptionalIntParameter(
        default=None,
        description="index of the block to run, used for GP scanning; default is None"
    )
    
    name_ext = luigi.OptionalStrParameter(
        default=".",
        description="extension to add to the name; default is an empty string"
    )
    
    is_all = luigi.BoolParameter(
        default=False,
        description="run all POIs simultaneously; default is False"
    ) # NOTE this is different to the entire_model parameter, which is used by workflow tasks
    
    def __init__(self, *args, **kwargs):
        entire_model = kwargs.pop("entire_model", False)
        super().__init__(*args, **kwargs)
        
        # Process pois, including the flag to use the entire model
        if entire_model:
            self.pois_split = self.COMBINE_POIS.split(',')
            self.pois = self.COMBINE_POIS
        else:
            self.pois_split = str(self.pois).split(',')
        if self.is_all:
            self.POI_NAME_STR = "all"
        else:
            self.POI_NAME_STR = "_".join(self.pois_split)
        self.POIS_TO_RUN = " ".join([f"-P {poi}" for poi in self.pois_split])
        for poi in self.pois_split:
            assert poi in self.COMBINE_POIS.split(','), f"POI {poi} not in model POIs {self.COMBINE_POIS}"
    
class GenerateRandom(POITask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pois_split = self.pois.split(',')

    def output(self):
        targets = []
        n_jobs = int(np.ceil(self.n_points / self.points_per_job))
        start = 0
        for i in range(n_jobs):
            end = min(start + (self.points_per_job-1), self.n_points-1)
            targets.append(self.local_target(f"random_points{self.name_ext}{'_'.join(self.pois_split)}_{start}_{end}.txt"))
            start += self.points_per_job
        targets.append(self.local_target(f"random_points{self.name_ext}{'_'.join(self.pois_split)}.txt"))
        return targets
    
    def run(self):      
        # Generate random points in the bounds
        poi_idxs = [self.COMBINE_POIS.split(',').index(poi) for poi in self.pois_split]
        bounds = self.bounds[poi_idxs]
        points = np.random.uniform(bounds[:, 0], bounds[:, 1], (self.n_points, len(self.pois_split)))

        # Write to output to the correct files
        for i, target in enumerate(self.output()[:-1]):
            target = self.output()[i]
            assert isinstance(target, law.LocalFileTarget)
            with open(target.path, 'w') as f:
                assert isinstance(f, TextIOWrapper)
                f.write(self.pois + '\n')
                for j in range(i*self.points_per_job, min((i+1)*self.points_per_job, self.n_points)):
                    f.write(','.join(map(str, points[j])) + '\n')
        
        target = self.output()[-1]
        assert isinstance(target, law.LocalFileTarget)
        with open(target.path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            f.write(self.pois + '\n')
            for point in points:
                f.write(','.join(map(str, point)) + '\n')

class GenerateGaussianProcess(POITask, HTCondorGPU):
    def create_branch_map(self):
        return [None] # Single branch, no special data
            
    def output(self):
        targets = []
        n_jobs = int(np.ceil(self.n_points / self.points_per_job))
        start = 0
        for i in range(n_jobs):
            end = min(start + (self.points_per_job-1), self.n_points-1)
            targets.append(self.local_target(f"gp_points{self.name_ext}{'_'.join(self.pois_split)}_{start}_{end}.txt"))
            start += self.points_per_job
        targets.append(self.local_target(f"gp_points{self.name_ext}{'_'.join(self.pois_split)}.txt"))
        return targets
    
    def run(self):
        assert self.block_index >= 1, "Cannot update Gaussian process for block 0, use GaussianProcessBase instead"
        
        # Parse the bounds
        pois = self.COMBINE_POIS.split(',')
        bounds = self.bounds
        ranges = bounds[:, 1] - bounds[:, 0]
        mins = bounds[:, 0]
        
        # Loop over all previous blocks
        data = pd.DataFrame()
        data_path = os.path.join(os.getenv("ANALYSIS_PATH"), 'data', 'HaddPOIs')
        scan_pattern = f"scan.GP_*.{self.channel}.{self.model}.*.{self.POI_NAME_STR}.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root"
        files = glob.glob(os.path.join(data_path, scan_pattern))
        for path in files:
            # Read the block's output
            file = uproot.open(path)
            
            # Access the values from the root file
            tree = file["limit"]
            block_data = pd.DataFrame(tree.arrays(pois + ['deltaNLL'], library="pd"))

            # Concatenate the block's data to the DataFrame
            data = pd.concat([data, block_data])
        data = data.drop_duplicates().reset_index(drop=True)
        
        # Drop large deltaNLL values
        data = data[data['deltaNLL'] <= 999]

        # Setup gaussian processes
        train_x = normalise(torch.from_numpy(data[pois].values), mins, ranges)
        train_y = torch.from_numpy(data['deltaNLL'].values) / data['deltaNLL'].max()
        print(f"5 sigma level: {25/data['deltaNLL'].max()}")
        training_iter = 200
        next_pts = []
        next_ys = []
        # print(bounds, ranges, mins)
        
        # Fit to the data and get the next n_batch points
        k = 0
        next_pts = []
        next_ys = []
        should_refit = True

        likelihood = gpytorch.likelihoods.FixedNoiseGaussianLikelihood(noise=torch.full_like(train_y, 1e-8))
        nn = min(train_x.shape[0] - 1, 50) 
        model = GPModel(inducing_points=train_x, likelihood=likelihood, k=nn, training_batch_size=nn)

        mll = gpytorch.mlls.VariationalELBO(likelihood, model, num_data=train_y.size(0))
        assert model.likelihood is not None
        optimizer = torch.optim.Adam(model.parameters(), lr=5e-2)
        scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.98)
        early_stopper = EarlyStopper(patience=5, min_delta=10)
        
        print("CUDA available:", torch.cuda.is_available())
        
        while k < self.points_per_block:
            if torch.cuda.is_available():
                likelihood = likelihood.cuda()
                model = model.cuda()
                train_x = train_x.cuda()
                train_y = train_y.cuda()
            
            if k != 0:
                training_iter = 50
            # print(train_x.detach(), train_y.detach())
            if should_refit:
                model.train()
                likelihood.train()
                for i in range(training_iter):
                    # Zero gradients from previous iteration
                    optimizer.zero_grad()
                    # Calc loss and backprop gradients
                    output = model(train_x)
                    _mll = mll(output, train_y)
                    assert isinstance(_mll, torch.Tensor)
                    loss = -_mll
                    if early_stopper.early_stop(loss):
                        print(f"Early stopping at iteration {i}")
                        break
                    loss.backward()
                    optimizer.step()
                    scheduler.step()
                    if i % 25 == 0:
                        print(i, loss.item(), optimizer.param_groups[0]['lr'])

            # Choose the next point to evaluate
            model.eval()
            likelihood.eval()
            with torch.no_grad(), gpytorch.settings.fast_pred_var(), gpytorch.settings.cholesky_jitter(1e-1):
                test_x = torch.tensor(np.random.uniform(0, 1, size=(2000, bounds.shape[0])))
                if torch.cuda.is_available():
                    test_x = test_x.cuda()
                posterior = model(test_x.float())
                
                # Mask high mean points
                test_x = test_x[posterior.mean < 50 / data['deltaNLL'].max()]
                posterior = model(test_x.float())
                
                # Get point with highest variance
                _, idx = torch.max(posterior.variance, dim=0)
                next_X = test_x[idx]
                next_y = posterior.mean[idx].cpu()
                next_y_var = posterior.variance[idx].cpu()
                
                # Throw a toy
                toy = np.random.normal(loc=next_y, scale=np.sqrt(next_y_var))
                if (toy <= (25 / data['deltaNLL'].max())) or (next_y <= (25 / data['deltaNLL'].max())):
                    k += 1
                    print(f"Got {k} points")
                
                    next_pts.append(next_X.cpu().detach().numpy())
                    next_ys.append(next_y.cpu().detach().numpy())
                    should_refit = True
                    print(f"Picked {unnormalise(next_X.cpu().detach().numpy(), mins, ranges)}, mean={next_y}, std={np.sqrt(next_y_var)}, threw {toy}")
                else:
                    print(f"Rejected point, toy={toy}, mean={next_y}, std={np.sqrt(next_y_var)}")
                    should_refit = False

                # Add the point to the training set (temporarily) so we don't sample it again
                train_x = torch.cat([train_x, next_X.unsqueeze(0).cuda()])
                train_y = torch.cat([train_y, next_y.unsqueeze(-1).cuda()])
                
                # Update the model with the new point, rather than cold-starting
                to_update = ['variational_strategy.inducing_points', 'variational_strategy._variational_distribution.variational_mean', 'variational_strategy._variational_distribution._variational_stddev']
                new_state_dict = model.state_dict().copy()
                for key, val in new_state_dict.items():
                    if key in to_update:
                        if 'inducing_points' in key:
                            new_state_dict[key] = train_x
                        elif 'variational_mean' in key:
                            new_state_dict[key] = torch.cat([new_state_dict[key], torch.tensor(0).unsqueeze(0).cuda()])
                        elif 'variational_stddev' in key:
                            new_state_dict[key] = torch.cat([new_state_dict[key], torch.tensor(1e-3).unsqueeze(0).cuda()])

                likelihood = gpytorch.likelihoods.FixedNoiseGaussianLikelihood(noise=torch.full_like(train_y, 1e-8))
                nn = min(train_x.shape[0] - 1, 50) 
                model = GPModel(inducing_points=train_x, likelihood=likelihood, k=nn, training_batch_size=nn)

                mll = gpytorch.mlls.VariationalELBO(likelihood, model, num_data=train_y.size(0))
                assert model.likelihood is not None
                optimizer = torch.optim.Adam(model.parameters(), lr=1e-2) # TODO rescale to 'fix' lr?
                scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.98)
                early_stopper = EarlyStopper(patience=5, min_delta=10)
                model.load_state_dict(new_state_dict)

        # Write to output to the correct files
        points = np.array(next_pts)
        for i, target in enumerate(self.output()[:-1]):
            target = self.output()[i]
            assert isinstance(target, law.LocalFileTarget)
            with open(target.path, 'w') as f:
                assert isinstance(f, TextIOWrapper)
                f.write(self.pois + '\n')
                for j in range(i*self.points_per_job, min((i+1)*self.points_per_job, self.n_points)):
                    f.write(','.join(map(str, points[j])) + '\n')
        
        target = self.output()[-1]
        assert isinstance(target, law.LocalFileTarget)
        with open(target.path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            f.write(self.pois + '\n')
            for point in points:
                f.write(','.join(map(str, point)) + '\n')

class ScanPOIs(POITask, HTCondorCPU, law.LocalWorkflow):
    """
    Class for running a POI scan
    """
    
    def create_branch_map(self):
        return {i: i for i in range(int(np.ceil(self.n_points / self.points_per_job)))}
    
    def workflow_requires(self):
        reqs = {'init': InitialFit.req(self)}
        if self.scan_method == 'rand':
            reqs['file'] = GenerateRandom.req(self, pois=self.pois, n_points=self.n_points, name_ext=self.name_ext)
        elif self.scan_method == 'GP':
            reqs['file'] = GenerateGaussianProcess.req(self)
        return reqs
    
    def requires(self):
        reqs = {'init': InitialFit.req(self)}
        if self.scan_method == 'rand':
            reqs['file'] = GenerateRandom.req(self, pois=self.pois, n_points=self.n_points, name_ext=self.name_ext)
        elif self.scan_method == 'GP':
            reqs['file'] = GenerateGaussianProcess.req(self)
        return reqs
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Process arguments
        self.start = self.branch * self.points_per_job
        self.end = min(self.start + (self.points_per_job-1), self.n_points-1)
        self.scan_algos = {
            'grid': 'grid',
            'rand': 'fixed',
            'GP'  : 'fixed'
        }
        self.algo = self.scan_algos.get(self.scan_method)
        if self.algo is None:
            raise ValueError(f"Scan method {self.scan_method} not recognised")
        if self.algo == 'fixed':
            try:
                file_target = self.input()['file'][self.branch]
            except KeyError:
                # Guess that file target is a workflow
                file_target = self.input()['file']['collection'][0][self.branch]
            assert isinstance(file_target, law.LocalFileTarget)
            self.file = file_target.path
        else:
            self.file = None
        self.FILE_STR = f"--fromfile {self.file}" if self.file is not None else ""
        self.POINTS_STR = f"{self.end - self.start + 1}" if self.file is not None else f"{self.n_points}"
        
        # Define the base command, handling only the branches, not the workflow itself
        if self.branch != -1:
            target = self.input()['init']['tree']
            assert isinstance(target, law.LocalFileTarget)
            self.initial_path = target.path
        
            # Build strings
            self.SKIP_OPTIONS = "--skipInitialFit"
            self.GENERATE_STR = "d;D;n;"
            if 'observed' in self.types: self.GENERATE_STR += f";{self.initial_path},data_obs,observed"
            if 'prefit_asimov' in self.types: self.GENERATE_STR += f";{self.initial_path},toys/toy_asimov,prefit_asimov"
            if 'postfit_asimov' in self.types: self.GENERATE_STR += f";{self.initial_path},toys/toy_asimov,postfit_asimov"
            
            self.ATTRIBUTES_STR = "freezeWithAttributes;n;"
            if "nominal" in self.attributes: self.ATTRIBUTES_STR += ";,nominal"
            if "fr.all" in self.attributes: self.ATTRIBUTES_STR += ";all,fr.all"
            if "fr.sigth" in self.attributes: self.ATTRIBUTES_STR += ";sigTheory,fr.sigth"
            if "fr.sigbkgth" in self.attributes: 
                # Requires doubling of commas to account for two frozen attributes
                self.ATTRIBUTES_STR = re.sub(",", ",,", self.ATTRIBUTES_STR)
                self.ATTRIBUTES_STR += ";sigTheory,bkgTheory,,fr.sigbkgth"
            self.GENERATOR = f"\"{self.GENERATE_STR}\" \"{self.ATTRIBUTES_STR}\" {self.FILE_STR}"
            
    def build_command(self):
        self.cmd = self.base_command
        self.cmd += (
            f" {self.time_command} combineTool.py -M MultiDimFit -m {self.MH}"
            f" --generate {self.GENERATOR}"
            f" --freezeParameters MH{self.COMBINE_FREEZE} --redefineSignalPOIs {self.COMBINE_POIS}"
            f" --setParameterRanges {self.COMBINE_RANGES} {self.COMBINE_OPTIONS}"
            f" -n .scan{self.name_ext}{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.{self.start}.{self.end}"
            f" --snapshotName \"MultiDimFit\" --algo {self.algo} --saveInactivePOI 1"
            f" {self.SKIP_OPTIONS} {self.COMBINE_SET_OPTIONS}"
            f" --points {self.POINTS_STR} --alignEdges 1 {self.POIS_TO_RUN}"
            f" --firstPoint {self.start} --lastPoint {self.end}"
            f"&> {self.output().dirname}/scan_{self.name_ext}_{self.channel}_{self.model}_{self.scan_method}_{self.POI_NAME_STR}_local.{self.branch}.log;"
        )
        
        if self.file is not None:
            input_files = ""
            for i in range(self.end - self.start + 1):
                input_files += os.path.join(os.getenv('ANALYSIS_PATH'), 
                                            f'higgsCombine.scan{self.name_ext}{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.{self.start}.{self.end}.{self.types}.{self.attributes}.POINTS.{i}.{i}.MultiDimFit.mH125.38.root ')
            self.cmd += f"hadd -k -f {self.output().basename} {input_files};"
            self.cmd += f"rm {input_files};"
        
        self.cmd += f"mv {self.output().basename} {self.output().path}"
        
    def output(self):
        return self.local_target(f"higgsCombine.scan{self.name_ext}{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.{self.start}.{self.end}.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root")
    
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois}, will output {self.output()}")
        self.build_command()
        self.run_cmd(self.cmd)

class ScanBlock(POITask):
    block_index = luigi.IntParameter()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_method = 'GP' if self.block_index > 0 else 'rand'
        self.block_task = HaddPOIs.req(self, scan_method=self.scan_method, 
                                       n_points=self.points_per_block,
                                       name_ext=f".GP_{self.block_index}.")
        
    def requires(self):
        if self.block_index == 0:
            return []
        else:
            return ScanBlock.req(self, block_index=self.block_index-1)
    
    def output(self):
        return self.block_task.output()

    def run(self):
        # Run the block by spawning the last task in the chain
        yield self.block_task
    
class ScanBlocks(law.WrapperTask, POITask):
    def requires(self):
        return ScanBlock.req(self, block_index=self.block_index)
    
    def output(self):
        return {
            'collection' : law.TargetCollection(self.collect_block_outputs(self.block_index))
            }

    def collect_block_outputs(self, block_index):
        if block_index < 0:
            return {}
        else:
            scan_block = ScanBlock.req(self, block_index=block_index)
            return {
                f"block_{block_index}": scan_block.block_task.output(),
                **self.collect_block_outputs(block_index - 1)
            }

class HaddPOIs(POITask):
    def requires(self):
        if self.scan_method == 'GP_blocks':
            if self.points_per_block is None:
                raise ValueError("GP scanning requires points_per_block to be set")
            return ScanBlocks.req(self, block_index=int(np.ceil(self.n_points/self.points_per_block))-1)
        else:
            return ScanPOIs.req(self, branch=-1)
    
    def output(self):
        return self.local_target(f"scan{self.name_ext}{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root")
    
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois}, will output {self.output()}")
        scan_collection = self.input()['collection']
        assert isinstance(scan_collection, law.TargetCollection)
        # TODO don't use private attributes
        input_paths = list(map(lambda t: t.path, scan_collection._flat_target_list))
        cmd = self.base_command
        cmd += f"hadd -k -f {self.output().path} {' '.join(input_paths)};"
        self.run_cmd(cmd)
        
class PlotPOIs(POITask):
    def requires(self):
        return HaddPOIs.req(self)
    
    def output(self):
        exts = ['png', 'pdf', 'root']
        plots = [self.local_target(f"scan_{self.channel}_{self.model}_{self.scan_method}_{self.POI_NAME_STR}.{ext}") for ext in exts]
        if len(self.pois_split) == 1:
            plots.append(self.local_target(f"{self.types}_{self.channel}_{self.model}_{self.scan_method}_{self.POI_NAME_STR}.json"))
        return plots
        
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois}, will output {self.output()}")
        hadd_target = self.input()
        assert isinstance(hadd_target, law.LocalFileTarget)
        
        if len(self.pois_split) == 1:
            plotting_script = 'plot1DScan.py'
            
            # Configure plot optons
            MAIN_OPTIONS_DICT = {
                "observed":"--main-label \"Observed\" --main-color 1",
                "postfit_asimov":"--main-label \"SM Expected (postfit)\" --main-color 2",
                "prefit_asimov":"--main-label \"SM Expected (prefit)\" --main-color 4"
            }
            MAIN_OPTIONS = MAIN_OPTIONS_DICT[self.types]
            plotting_options = (
                f"--paper -o {os.path.splitext(self.output()[0].basename)[0]} --POI {self.pois} --model {self.model} "
                f"--json {self.output()[-1].path} "
                f"-m {hadd_target.path} --remin-main --remove-delta 1E-6 --improve --y-max 20 "
                f"--chop 20 {MAIN_OPTIONS} --no-input-label --outdir {self.output()[0].dirname}"
            )
            
        elif len(self.pois_split) == 2:
            # Get the x and y ranges
            range_strs = self.COMBINE_RANGES.split(':')
            for range_str in range_strs:
                if self.pois_split[0] in range_str:
                    x_range = range_str.strip(self.pois_split[0]+'=')
                if self.pois_split[1] in range_str:
                    y_range = range_str.strip(self.pois_split[1]+'=')
            
            plotting_script = 'generic2D.py'
            plotting_options = (
                f"-o {os.path.splitext(self.output()[0].basename)[0]} -f {hadd_target.path} "
                f"--remin --sm-point 0,0 --translate pois.json "
                f"--x-axis {self.pois_split[0]} --y-axis {self.pois_split[1]} "
                f"--x-range=\"{x_range}\" --y-range=\"{y_range}\" "
            )
            plotting_options += f"; mv {os.path.splitext(self.output()[0].basename)[0]}* {self.output()[0].dirname};"
        else:
            raise ValueError(f"Cannot plot {len(self.pois_split)} (as >2) POIs")
        
        cmd = self.base_command
        cmd += f"python3 {plotting_script} {plotting_options}"
        self.run_cmd(cmd)

class ScanSingles(POITask):
    """
    Takes a model and a number of points, performs a 1D profiled scan of each POI
    """
    notify_slack = NotifySlackParameterUTF8()
    split_timer = SplitTimeDecorator()
    
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
    @split_timer
    def requires(self, *args, **kwargs):
        # Each branch requires the scan for the corresponding POI
        return {poi: PlotPOIs.req(self, pois=poi, n_points=self.n_points) for poi in self.pois_split}
    
    def output(self):
        return {
            'log' : self.local_target(f"singles.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.txt"),
            'limits' : self.local_target(f"singles.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.json")
        }
        
    @split_timer
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois_split}, will output {self.output()}")
        # Log to file
        with open(self.output()['log'].path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            for poi in self.pois_split:
                scan_target = self.input()[poi][0]
                assert isinstance(scan_target, law.LocalFileTarget)
                f.write(f"{poi} {scan_target.path}\n")
                
        # Grab and merge the jsons
        jsons = [self.input()[poi][-1] for poi in self.pois_split]
        merged_data = {}
        for file in jsons:
            assert isinstance(file, law.LocalFileTarget)
            with open(file.path, 'r') as f:
                data = json.load(f)
                deep_merge(merged_data, data)
        with open(self.output()['limits'].path, 'w') as f:
            json.dump(merged_data, f, indent=4)

class ScanPairs(POITask):
    """
    Takes a model and a number of points, performs a 2D profiled scan of each pair of POIs
    """
    notify_slack = NotifySlackParameterUTF8()
    split_timer = SplitTimeDecorator()
    
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
        # Compute pairs
        # TODO test a model with only one POI
        self.poi_pairs = list(map(','.join, list(combinations(self.pois_split, 2))))
        
    @split_timer
    def requires(self):
        # Each branch requires the scan for the corresponding POI
        return {pair: PlotPOIs.req(self, pois=pair, n_points=self.n_points) for pair in self.poi_pairs}
    
    def output(self):
        return self.local_target(f"pairs.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.txt")
    
    @split_timer
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.poi_pairs}, will output {self.output()}")
        # Write to file
        with open(self.output().path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            for pair in self.poi_pairs:
                scan_target = self.input()[pair][0]
                assert isinstance(scan_target, law.LocalFileTarget)
                f.write(f"{pair} {scan_target.path}\n")

class ScanAll(POITask):
    """
    Take a model and a number of points, perform a scan of all POIs simultaneously
    """
    notify_slack = NotifySlackParameterUTF8()
    split_timer = SplitTimeDecorator()
    
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True, is_all=True))
    
    @split_timer  
    def requires(self):
        # Each branch requires the scan for the corresponding POI
        return {'all': HaddPOIs.req(self, pois=self.COMBINE_POIS, n_points=self.n_points, is_all=True)}

    def output(self):
        return self.local_target(f"all.{self.channel}.{self.model}.{self.scan_method}.{self.types}.{self.attributes}.txt")
    
    @split_timer
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.model}, will output {self.output()}")
        # Write to file
        with open(self.output().path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            scan_target = self.input()['all']
            assert isinstance(scan_target, law.LocalFileTarget)
            f.write(f"all {scan_target.path}\n")
