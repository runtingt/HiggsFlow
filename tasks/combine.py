import os
import re
import law
import luigi
import shutil
import numpy as np
from io import TextIOWrapper
from typing import Dict
from getPOIs import GetWsp, GetT2WOpts, GetMinimizerOpts, GetPOIsList, GetPOIRanges, GetFreezeList
from tasks.base import ForceableWithNewer
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
        # self.COMBINE_POIS_TO_RUN = GetGeneratePOIs(self.model)
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

    scan_method = luigi.Parameter(
        default="grid",
        description="scan method to use; default is grid"
    )
    
    def __init__(self, *args, **kwargs):
        entire_model = kwargs.pop("entire_model", False)
        super().__init__(*args, **kwargs)
        
        # Process pois, including the flag to use the entire model
        if entire_model:
            self.pois_split = self.COMBINE_POIS.split(',')
            self.pois = self.COMBINE_POIS
        else:
            self.pois_split = str(self.pois).split(',')
        self.POIS_TO_RUN = " ".join([f"-P {poi}" for poi in self.pois_split])
        self.POI_NAME_STR = "_".join(self.pois_split)
        for poi in self.pois_split:
            assert poi in self.COMBINE_POIS.split(','), f"POI {poi} not in model POIs {self.COMBINE_POIS}"
    
class GenerateRandom(CombineBase):
    def __init__(self, *args, **kwargs):
        self.pois = str(kwargs.pop("pois", "r")).split(',')
        self.n_points = kwargs.pop("n_points", 10)
        super().__init__(*args, **kwargs)
    
    def output(self):
        return self.local_target(f"random_points_{'_'.join(self.pois)}.txt")
    
    def run(self):
        # Get poi bounds
        bound_strs = self.COMBINE_RANGES.split(':')
        bounds = []
        for poi, bound_str in zip(self.pois, bound_strs):
            assert poi in bound_str, f"{self.pois} does not match {bound_strs}"
            lo, hi = map(float, bound_str.strip(poi+'=').split(','))
            bounds.append(np.array([lo, hi]))
        bounds = np.array(bounds)
        
        # Generate random points in the bounds
        points = np.random.uniform(bounds[:,0], bounds[:,1], (self.n_points, len(self.pois)))

        # Write to output as csv with pois as columns
        with open(self.output().path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            f.write(','.join(self.pois) + '\n')
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
            reqs['file'] = GenerateRandom.req(self, pois=self.pois, n_points=self.n_points)
        return reqs
    
    def requires(self):
        reqs = {'init': InitialFit.req(self)}
        if self.scan_method == 'rand':
            reqs['file'] = GenerateRandom.req(self, pois=self.pois, n_points=self.n_points)
        return reqs
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Process arguments
        self.scan_algos = {
            'grid': 'grid',
            'rand': 'fixed'
        }
        self.algo = self.scan_algos.get(self.scan_method)
        if self.algo is None:
            raise ValueError(f"Scan method {self.scan_method} not recognised")
        if self.scan_method == 'rand':
            file_target = self.input()['file']
            assert isinstance(file_target, law.LocalFileTarget)
            self.file = file_target.path
        else:
            self.file = None
        self.FILE_STR = f"--fromfile {self.file}" if self.file is not None else ""
        
        self.start = self.branch * self.points_per_job
        self.end = min(self.start + (self.points_per_job-1), self.n_points-1)
        
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
            f" -n .scan.{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.{self.start}.{self.end}"
            f" --snapshotName \"MultiDimFit\" --algo {self.algo} --saveInactivePOI 1"
            f" {self.SKIP_OPTIONS} {self.COMBINE_SET_OPTIONS}"
            f" --points {self.n_points} --alignEdges 1 {self.POIS_TO_RUN}"
            f" --firstPoint {self.start} --lastPoint {self.end}"
            f"&> {self.output().dirname}/scan_{self.channel}_{self.model}_{self.scan_method}_{self.POI_NAME_STR}_local.log;"
        )
        
        if self.file is not None:
            input_files = ""
            for i in range(self.start, self.end + 1):
                input_files += os.path.join(os.getenv('ANALYSIS_PATH'), 
                                            f'higgsCombine.scan.{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.{self.start}.{self.end}.{self.types}.{self.attributes}.POINTS.{i}.{i}.MultiDimFit.mH125.38.root ')
            self.cmd += f"hadd -k -f {self.output().basename} {input_files};"
            self.cmd += f"rm {input_files};"
        
        self.cmd += f"mv {self.output().basename} {self.output().path}"
        
    def output(self):
        return self.local_target(f"higgsCombine.scan.{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.{self.start}.{self.end}.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root")
    
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois}, will output {self.output()}")
        self.build_command()
        self.run_cmd(self.cmd)

class HaddPOIs(POITask):
    def requires(self):
        return ScanPOIs.req(self, branch=-1)
    
    def output(self):
        return self.local_target(f"scan.{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root")
    
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois}, will output {self.output()}")
        scan_collection = self.input()['collection']
        assert isinstance(scan_collection, law.TargetCollection)
        scan_target = scan_collection.first_target
        assert isinstance(scan_target, law.LocalFileTarget)
        input_files = os.path.join(scan_target.dirname,
                                   f"higgsCombine.scan.{self.channel}.{self.model}.{self.scan_method}.{self.POI_NAME_STR}.POINTS.*.{self.types}.{self.attributes}.MultiDimFit.mH{self.MH}.root")
        cmd = self.base_command
        cmd += f"hadd -k -f {self.output().path} {input_files};"
        self.run_cmd(cmd)
        
class PlotPOIs(POITask):
    def requires(self):
        return HaddPOIs.req(self)
    
    def output(self):
        exts = ['png', 'pdf', 'root']
        plots = [self.local_target(f"scan_{self.channel}_{self.model}_{self.scan_method}_{self.POI_NAME_STR}.{ext}") for ext in exts]
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
                f"--json {self.output()[0].dirname}/{self.types}_{self.pois}.json "
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
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
    def requires(self):
        # Each branch requires the scan for the corresponding POI
        return {poi: PlotPOIs.req(self, pois=poi, n_points=self.n_points) for poi in self.pois_split}
    
    def output(self):
        return self.local_target(f"singles.txt")
    
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.pois_split}, will output {self.output()}")
        # Write to file
        with open(self.output().path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            for poi in self.pois_split:
                scan_target = self.input()[poi][0]
                assert isinstance(scan_target, law.LocalFileTarget)
                f.write(f"{poi} {scan_target.path}\n")

class ScanPairs(POITask):
    """
    Takes a model and a number of points, performs a 2D profiled scan of each pair of POIs
    """
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
        # Compute pairs
        from itertools import combinations
        self.poi_pairs = list(map(','.join, list(combinations(self.pois_split, 2))))
        
    def requires(self):
        # Each branch requires the scan for the corresponding POI
        return {pair: PlotPOIs.req(self, pois=pair, n_points=self.n_points) for pair in self.poi_pairs}
    
    def output(self):
        return self.local_target(f"pairs.txt")
    
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
    def __init__(self, *args, **kwargs):
        # Just pass in the model's pois
        # TODO can we do this in a cleaner way?
        super().__init__(*args, **dict(kwargs, entire_model=True))
        
    def requires(self):
        # Each branch requires the scan for the corresponding POI
        return {'all': ScanPOIs.req(self, pois=self.COMBINE_POIS, n_points=self.n_points)}
    
    def output(self):
        return self.local_target(f"all.txt")
    
    def run(self):
        logger.info(f"Running: {self.__class__.__name__} for {self.model}, will output {self.output()}")
        # Write to file
        with open(self.output().path, 'w') as f:
            assert isinstance(f, TextIOWrapper)
            scan_target = self.input()['all'][0]
            assert isinstance(scan_target, law.LocalFileTarget)
            f.write(f"all {scan_target.path}\n")
