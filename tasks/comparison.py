import law
import luigi
import json
import numpy as np
import mplhep as hep
import uproot
import pandas as pd
import pickle
from scipy.stats import norm
from interpolator.base import Interpolator
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from collections import defaultdict
from tasks.base import ForceableWithNewer
from tasks.utils import colors
from tasks.models import BuildModel, models_dict

hep.style.use(hep.style.CMS)
    
# TODO make checkers for model and comparison dicts 
comparisons_dict = {
    'hgg_statonly2D' : {
        'truth' : {
            '1DScans' : 'hgg_statonly2D_grid_truth',
            '2DScans' : 'hgg_statonly2D_grid_truth',
            'nDScans' : 'hgg_statonly2D_rand_truth',
            'nDEval'  : 'hgg_statonly2D_rand_truth',
            },
        'approximations' : {
            'grid_interp' : {
                '1DScans' : 'hgg_statonly2D_grid_interp',
                '2DScans' : 'hgg_statonly2D_grid_interp',
                'nDScans' : 'hgg_statonly2D_grid_interp',
                'nDEval'  : 'hgg_statonly2D_grid_interp',
                },
            'STXS' : {
                '1DScans' : 'hgg_statonly2D_STXS',
                '2DScans' : 'hgg_statonly2D_STXS',
                'nDScans' : 'hgg_statonly2D_STXS',
                'nDEval'  : 'hgg_statonly2D_STXS',
                },
            'SMEFT' : {
                '1DScans' : 'hgg_statonly2D_SMEFT',
                '2DScans' : 'hgg_statonly2D_SMEFT',
                'nDScans' : 'hgg_statonly2D_SMEFT',
                'nDEval'  : 'hgg_statonly2D_SMEFT',
                },
            }
        }
    }

class BuildComparison(ForceableWithNewer):
    comparison_name = luigi.Parameter(
        description="The comparison to build. Must be a " \
            "key defined in comparisons_dict."
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.comparison = comparisons_dict[self.comparison_name]
        except KeyError:
            raise KeyError(f"Comparison {self.comparison_name} not found in {comparisons_dict.keys()}")
    
    def requires(self):
        truth_models = dict(self.comparison['truth'])
        approx_models = dict(self.comparison['approximations'])
        return ({key: BuildModel(model_name=model) for key, model in truth_models.items()} |
                {approx_model_name : {key: BuildModel(model_name=model) for key, model in dict(approx_model_vals).items()} 
                 for approx_model_name, approx_model_vals in approx_models.items()})
    
    def output(self):
        return self.local_target(f"{self.comparison_name}.json")
    
    def run(self):
        with open(self.output().path, 'w') as f:
            json.dump(self.comparison, f, indent=4)

class Compare(ForceableWithNewer):   
    comparison_name = luigi.Parameter(
        description="The model to use as the 'truth' dataset. Must be a " \
            "key defined in comparisons_dict."
    )
    
    def initialise(self):
        # Unpack the model
        with open(BuildComparison(comparison_name=self.comparison_name).output().path, 'r') as f:
            self.comparison = dict(json.load(f))
        self.truth_model = dict(self.comparison['truth'])
        self.approx_models = dict(self.comparison['approximations'])

        # Get the POIs from the truth model
        self.pois = list(self.process_limit(models_dict[self.truth_model['1DScans']].get_reqs()['1D'].output()['limits'],
                                            models_dict[self.truth_model['1DScans']].model).keys())
        
    def requires(self):
        return BuildComparison(comparison_name=self.comparison_name)
    
    def output(self):
        return {
            'fishbone': self.local_target(f"fishbone_{self.comparison_name}.png"),
            'diff1D': self.local_target(f"diff1D_{self.comparison_name}.png"),
            'corner': self.local_target(f"corner_{self.comparison_name}.png"),
        }
    
    def process_limit(self, limit_json: law.LocalFileTarget, model_name: str):
        results = defaultdict(lambda: defaultdict(dict))
        with open(limit_json.path, 'r') as f:
            poi_limits = dict(json.load(f)[model_name])
            for poi, limit_info in poi_limits.items():
                results[poi]['best'] = limit_info['Val']
                results[poi]['ci_0'] = [limit_info['Val'] + limit_info['ErrorLo'], 
                                        limit_info['Val'] + limit_info['ErrorHi']]
                results[poi]['ci_1'] = [limit_info['Val'] + limit_info['2sig_ErrorLo'],
                                        limit_info['Val'] + limit_info['2sig_ErrorHi']]
        return results
    
    def make_fishbone(self):
        # Extract models
        scan1D_models = {'truth' : models_dict[self.truth_model['1DScans']]}
        for name, approx_model in self.approx_models.items():
            scan1D_models[name] = models_dict[approx_model['1DScans']]
            
        # Extract limits
        results = defaultdict(lambda: defaultdict(dict))
        for name, model in scan1D_models.items():
            scan1D_limits = model.get_reqs()['1D'].output()['limits']
            assert isinstance(scan1D_limits, law.LocalFileTarget)
            results[name] = self.process_limit(scan1D_limits, model.model)
        
        # Plot
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))
        assert isinstance(ax, plt.Axes)
        xs = np.arange(len(self.pois))
        levels = [1, 4]
        ci_styles = ['-', '--']

        # Get shifts for each model
        padding = 0.97 # Space between the end of one block and the *center* of the next
        start = -(1-padding)
        end = -start
        shifts = np.linspace(start, end, len(results.keys()))

        # Plot best fits and CIs
        for i, (model, shift) in enumerate(zip(results.keys(), shifts)):
            # Extract the best fits
            best_fits = [results[model][poi]['best'] for poi in self.pois]
            ax.scatter(xs+shift, best_fits, s=100, zorder=2, c=colors[i])
            
            # Extract the CIs
            for j in range(len(levels)):
                ci = np.array([results[model][poi][f'ci_{j}'] for poi in self.pois]).T
                ax.plot([xs+shift, xs+shift], ci, c=colors[i], 
                        lw=5-2*j, ls=ci_styles[j])
            
            # For a nice legend
            ax.plot(0, lw=10, label=model, c=colors[i])
            
        # Add to legend
        ax.scatter(np.inf, np.inf, s=0,  c='k', label='\n')
        ax.scatter(np.inf, np.inf, s=100, c='k', label='Best fit')
        ax.plot(np.inf, ls='-', c='k', label=r'$68\%\;\mathrm{CL}$')
        ax.plot(np.inf, ls='--', c='k', label=r'$95\%\;\mathrm{CL}$')
        
        # Formatting
        ax.set_xlabel('Wilson Coefficient')
        ax.set_ylabel('Parameter value')
        ax.set_xticks(xs)
        ax.set_xticklabels(self.pois)
        ax.set_xlim((-0.5, xs.max()+1.5))
        ax.set_ylim(-30, 10)
        ax.legend(loc='upper right')
        plt.axhline(0, c='k', lw=2, zorder=-1)
        plt.tight_layout()
        plt.savefig(self.output()['fishbone'].path, dpi=125, bbox_inches='tight')
            
    def make_diff1D(self):
        # Get the truth likelihood values
        true_scan = models_dict[self.truth_model['nDScans']].get_reqs()['TruthND'].requires()['all']
        true_vals = true_scan.output()
        assert isinstance(true_vals, law.LocalFileTarget)
        file = uproot.open(true_vals.path)
        limit = file['limit']
        scan_df = pd.DataFrame(limit.arrays(self.pois + ['deltaNLL'], library='pd'))
        file.close()

        # Process dataframe
        scan_df.drop_duplicates(inplace=True)
        scan_df['deltaq'] = 2*(scan_df['deltaNLL'])
        mask = scan_df['deltaq'] < 10
        
        # For each approximate model, get its evaluator and evaluate at each point
        for approx_name, approx_model in self.approx_models.items():
            evaluator_target = models_dict[approx_model['nDEval']].get_reqs()['NDEval'].output()
            assert isinstance(evaluator_target, law.LocalFileTarget)
            with open(evaluator_target.path, 'rb') as f:
                evaluator = pickle.load(f)
                assert isinstance(evaluator, Interpolator)
            
            # Evaluate the interpolator at the scan points
            model_out = np.full(len(scan_df), np.inf)
            for i, pt in enumerate(scan_df[self.pois].to_numpy()):
                d = {k: [v] for k, v in zip(self.pois, pt)}
                model_out[i] = 2*evaluator.evaluate(pd.DataFrame(d))[0]
            scan_df[approx_name] = model_out
        print(scan_df[mask].describe())
        
        # Plot the difference to the test dataset in a histogram
        fig, axs = plt.subplots(1, 2, figsize=(32, 9))
        for i, key in enumerate(self.approx_models.keys()):
            error = scan_df["deltaq"][mask] - scan_df[key][mask]
            
            # Fit each distribution to a Gaussian
            xs = np.linspace(-10, 6, 1000)
            mu, std = norm.fit(error[~np.isnan(error)])
            
            # Plot each fit
            for ax, nbins in zip(axs, [50, 200]):
                assert isinstance(ax, plt.Axes)
                ax.plot(xs, norm.pdf(xs, mu, std), 
                        linestyle='--', c=colors[i+1], lw=2)
                ax.hist(error, label=rf"{key}, $\mu={{{mu:.3f}}}, \sigma={{{std:.3f}}}$",
                        range=(-10, 10), color=colors[i+1],
                        bins=nbins, histtype='step', lw=2, density=True)
            ax.set_xlim(-2, 1)

        # Annotate
        for ax in axs:
            assert isinstance(ax, plt.Axes)
            ax.text(1-0.0125, 0.925, r"$\Delta q < 10$", transform=ax.transAxes,
                    ha="right", fontstyle='italic')
            ax.legend(loc='upper left')
            # ax.set_ylim(0, 5)
            ax.set_xlabel(r"$True\;\Delta q - Model\;\Delta q$")
            ax.set_ylabel("Density")
        plt.tight_layout()
        plt.savefig(self.output()['diff1D'].path, dpi=125, bbox_inches='tight')
           
    def make_corner(self):   
        truth_single_plots = models_dict[self.truth_model['1DScans']].get_reqs()['1D'].requires()
        truth_pair_plots = models_dict[self.truth_model['1DScans']].get_reqs()['2D']
        
        # Get best fits
        best = {}
        for poi in self.pois:
            truth_single_plot = truth_single_plots[poi]
            truth_single = truth_single_plot.input()
            assert isinstance(truth_single, law.LocalFileTarget)
            file = uproot.open(truth_single.path)
            limit = file['limit']
            scan_df = pd.DataFrame(limit.arrays(library='pd'))
            file.close()
            best[poi] = scan_df[poi][scan_df['deltaNLL'] == 0].values[0]
           
        # Plot
        fig = plt.figure(figsize=(45, 30))
        gs = GridSpec(len(self.pois), len(self.pois), hspace=0., wspace=0.)
        for i in range(len(self.pois)):
            for j in range(len(self.pois)):
                ax = fig.add_subplot(gs[i*len(self.pois) + j])
                # Upper right triangle is disabled
                if j > i:
                    ax.axis('off')
                    # Add legend
                    if i == 0 and j == len(self.pois)-1:
                        ax.plot(np.inf, np.inf, lw=5, label='truth', c=colors[0])
                        for k, label in enumerate(self.approx_models.keys()):
                            ax.plot(np.inf, np.inf, lw=5, label=label, c=colors[k+1])
                        ax.legend(loc='upper right', handlelength=2, prop={'size': 54})
                        
                # Plot 1D
                elif j == i:  
                    # Get truth profiled scans
                    poi = self.pois[i]
                    truth_single_plot = truth_single_plots[poi]
                    truth_single = truth_single_plot.input()
                    assert isinstance(truth_single, law.LocalFileTarget)
                    file = uproot.open(truth_single.path)
                    limit = file['limit']
                    scan_df = pd.DataFrame(limit.arrays(library='pd'))
                    file.close()
                                                   
                    # Fit truth deltaNLL to a polynomial
                    scan_df.drop_duplicates(inplace=True)
                    mask = 2*scan_df['deltaNLL'] < 10
                    x = scan_df[self.pois[i]][mask]
                    y = scan_df['deltaNLL'][mask]
                    p = np.polyfit(x, y, 4)
                    x_fit = np.linspace(np.min(x), np.max(x), 1000)
                    y_fit = np.polyval(p, x_fit)
                    mask = 2*y_fit < 10
                    
                    # Plot
                    scatter_mask = 2*scan_df['deltaNLL'] < 10
                    ax.plot(x_fit[mask], 2*y_fit[mask], c=colors[0], lw=5)
                    ax.scatter(scan_df[self.pois[i]][scatter_mask], 2*scan_df['deltaNLL'][scatter_mask], c=colors[0], s=100)
                    
                    # Plot models
                    for k, approx_model in enumerate(self.approx_models.values()):
                        # Get the profile
                        approx_single = models_dict[approx_model['1DScans']].get_reqs()['1D'].output()['profiles'][poi]
                        assert isinstance(approx_single, law.LocalFileTarget)
                        profile = np.load(approx_single.path)
                        mask = profile[1] < 10
                        ax.plot(profile[0][mask], profile[1][mask], c=colors[k+1], lw=5)
                        
                    # Annotate
                    ax.set_ylim((0, 12))
                    ax.set_xlim(truth_single_plot.bounds[i][0]*1.05, truth_single_plot.bounds[i][1]*1.05)
                    shifts = [1.00, 4.00]
                    shiftlabels = ['68%', '95%']
                    for shift, label in zip(shifts, shiftlabels):
                        # Add horizontal lines
                        ax.plot([np.min(x)*2, np.max(x)*2], [shift, shift], 
                                lw=2.5, ls='-', c='k', alpha=0.1, zorder=-5)
                        ax.text(0.995, (shift+0.15)/ax.get_ylim()[1], 
                                f'{label}', transform=ax.transAxes,
                                horizontalalignment='right', 
                                fontsize=48, alpha=0.75)
                        ax.text(0.01, 0.975, r"$\Delta NLL$",
                                transform=ax.transAxes, horizontalalignment='left',
                                verticalalignment='top', fontweight='regular',
                                fontsize=54, alpha=0.4)
                    
                # Plot 2D
                else:
                    # Plot truth
                    contours = {}
                    pair = f"{self.pois[j]},{self.pois[i]}"
                    target_plot = truth_pair_plots.input()[pair][2]
                    assert isinstance(target_plot, law.LocalFileTarget)
                    file = uproot.open(target_plot.path)
                    cis = [68, 95]
                    for ci in cis: 
                        try:
                            contours[ci] = file[f'graph{ci}_default_0;1'].values()
                        except uproot.KeyInFileError:
                            print(f"Warning: no {ci}% CL contour found to add")
                    file.close()
                    for ci, ls in zip(cis, ['-', '--']):
                        try:
                            ax.plot(contours[ci][0], contours[ci][1], c=colors[0], lw=5, ls=ls)
                        except KeyError:
                            print(f"Warning: no {ci}% CL contour found to plot")
                    
                    # Plot models
                    for k, approx_model in enumerate(self.approx_models.values()):
                        # Load the interpolator
                        approx_pair = models_dict[approx_model['1DScans']].get_reqs()['2D'].output()['profiles'][pair]
                        assert isinstance(approx_pair, law.LocalFileTarget)
                        profile = np.load(approx_pair.path)
                        
                        shifts = [2.30, 6.18]
                        for shift, style in zip(shifts, ['-', '--']):
                            ax.contour(profile[0], profile[1], profile[2], 
                                       levels=[shift], colors=colors[k+1], 
                                       linestyles=style, linewidths=5)
                      
                    # Annotate
                    ax.set_xlim(truth_pair_plots.bounds[j][0]*1.05, truth_pair_plots.bounds[j][1]*1.05)
                    ax.set_ylim(truth_pair_plots.bounds[i][0]*1.05, truth_pair_plots.bounds[i][1]*1.05)
                    
                # Label
                if j == 0 and i != 0:
                    ax.set_ylabel(self.pois[i], fontsize=48)
                else:
                    ax.tick_params(labelleft=False)
                if i == len(self.pois)-1:
                    ax.set_xlabel(self.pois[j], fontsize=48)
                else:
                    ax.tick_params(labelbottom=False)
                ax.tick_params(labelsize=40)

        plt.savefig(self.output()['corner'].path, bbox_inches='tight', dpi=125)
    
    def run(self):
        self.initialise()
        self.make_fishbone()
        self.make_diff1D()
        self.make_corner()
