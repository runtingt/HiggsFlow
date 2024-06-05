import law
import luigi
import models
import json
import uproot
import pickle
import pandas as pd
import numpy as np
import mplhep as hep
from scipy.stats import norm
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from collections import defaultdict
from tasks.base import ForceableWithNewer
from tasks.interpolation import BuildInterpolator, InterpolateSingles, InterpolatePairs
from tasks.combine import PlotPOIs, ScanAll, ScanPairs, ScanSingles
from tasks.utils import colors
from interpolator.base import rbfInterpolator

hep.style.use(hep.style.CMS)

class Compare(ForceableWithNewer):
    models_to_compare = luigi.ListParameter(
        description="List of models to compare, where each entry is a " \
            "key defined in models.py",
        schema={
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    )
    
    truth_model = luigi.Parameter(
        description="The model to use as the 'truth' dataset. Must be a " \
            "key defined in models.py"
    )
        
    def requires(self):
        # TODO check models are compatible
        try:
            self.to_compare = {
                f'interp_{model}' : 
                    {
                        'singles' : InterpolateSingles(**models.models[model].to_params()),
                        'pairs' : InterpolatePairs(**models.models[model].to_params()),
                        'interp' : BuildInterpolator(**models.models[model].to_params())
                    } 
                    for model in self.models_to_compare
                }
            self.truth = {
                'all' : ScanAll(**models.models[self.truth_model].to_params()), 
                'pairs' : ScanPairs(**models.models[self.truth_model].to_params()),
                'singles' : ScanSingles(**models.models[self.truth_model].to_params())
                }
        except KeyError as e:
            raise ValueError(f"Model key {e} not found in {models.__file__}")
        return [self.to_compare, self.truth]

    def output(self):
        try:
            return {
                'fishbone' : self.local_target(f"fishbone_{models.models[self.truth_model].model}.png"),
                'diff1D' : self.local_target(f"diff1D_{models.models[self.truth_model].model}.png"),
                'corner' : self.local_target(f"corner_{models.models[self.truth_model].model}.png"),
            }
        except KeyError as e:
            raise ValueError(f"Model key {e} not found in {models.__file__}")
        
    def process_limit(self, limit_json: law.LocalFileTarget, key: str):
        results = defaultdict(lambda: defaultdict(dict))
        with open(limit_json.path, 'r') as f:
            poi_limits = dict(json.load(f)[models.models[self.truth_model].model])
            for poi, limit_info in poi_limits.items():
                results[poi]['best'] = limit_info['Val']
                results[poi]['ci_0'] = [limit_info['Val'] + limit_info['ErrorLo'], 
                                        limit_info['Val'] + limit_info['ErrorHi']]
                results[poi]['ci_1'] = [limit_info['Val'] + limit_info['2sig_ErrorLo'],
                                        limit_info['Val'] + limit_info['2sig_ErrorHi']]
        return results
    
    def make_fishbone(self):
        results = defaultdict(lambda: defaultdict(dict))
        
        # Parse the json file for the profiled fits from combine
        # TODO make sure limits are valid (at the moment we're using random for testing, 
        # we might be better off forcing this to use the grid)
        truth_limits = self.input()[-1]['singles']['limits']
        interp_limits_dict = self.input()[0]
        assert isinstance(interp_limits_dict, dict)
        interp_limits = [d['singles'] for d in interp_limits_dict.values()]
        limit_jsons = [truth_limits] + interp_limits
        results = defaultdict(lambda: defaultdict(dict))
        for limit_json, key in zip(limit_jsons, ['truth'] + list(interp_limits_dict.keys())):
            # Add to results
            results[key] = self.process_limit(limit_json, key)  
        
        # Plot
        pois = list(results['truth'].keys())
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))
        assert isinstance(ax, plt.Axes)
        xs = np.arange(len(pois))
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
            best_fits = [results[model][poi]['best'] for poi in pois]
            ax.scatter(xs+shift, best_fits, s=100, zorder=2, c=colors[i])
            
            # Extract the CIs
            for j in range(len(levels)):
                ci = np.array([results[model][poi][f'ci_{j}'] for poi in pois]).T
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
        ax.set_xticklabels(pois)
        ax.set_xlim((-0.5, xs.max()+1.5))
        ax.set_ylim(-30, 10)
        ax.legend(loc='upper right')
        plt.axhline(0, c='k', lw=2, zorder=-1)
        plt.tight_layout()
        plt.savefig(self.output()['fishbone'].path, dpi=125, bbox_inches='tight')
    
    def make_diff1D(self):
        # Get the truth likelihood values
        scan = self.requires()[-1]['all']
        assert isinstance(scan, ScanAll)
        scan_target = scan.input()['all']
        assert isinstance(scan_target, law.LocalFileTarget)
        file = uproot.open(scan_target.path)
        limit = file['limit']
        scan_df = pd.DataFrame(limit.arrays(scan.COMBINE_POIS.split(',') + ['deltaNLL'], library='pd'))
        file.close()
        
        # Process dataframe
        scan_df.drop_duplicates(inplace=True)
        scan_df['deltaq'] = 2*(scan_df['deltaNLL'])
        mask = scan_df['deltaq'] < 10
        
        # For each model, load its 'Interpolator' object and compute values
        # TODO better name?
        interp_limits = self.input()[0]
        assert isinstance(interp_limits, dict)
        for key, model_req in interp_limits.items():
            # Load the interpolator
            interp = model_req['interp']
            assert isinstance(interp, law.LocalFileTarget)
            with open(interp.path, 'rb') as f:
                interp = pickle.load(f)
            assert isinstance(interp, rbfInterpolator)
            
            # Evaluate the interpolator at the scan points
            model_out = np.full(len(scan_df), np.inf)
            for i, pt in enumerate(scan_df[scan.COMBINE_POIS.split(',')].to_numpy()):
                d = {k: [v] for k, v in zip(scan.COMBINE_POIS.split(','), pt)}
                model_out[i] = 2*interp.evaluate(pd.DataFrame(d))[0]
            scan_df[key] = model_out
        
        # Plot the difference to the test dataset in a histogram
        fig, axs = plt.subplots(1, 2, figsize=(32, 9))
        for i, key in enumerate(interp_limits.keys()):
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
        truth_singles = self.requires()[-1]['singles']
        truth_pairs = self.requires()[-1]['pairs']
        assert isinstance(truth_singles, ScanSingles)
        assert isinstance(truth_pairs, ScanPairs)
        pois = truth_singles.COMBINE_POIS.split(',')
        
        # Plot
        fig = plt.figure(figsize=(45, 30))
        gs = GridSpec(len(pois), len(pois), hspace=0., wspace=0.)
        for i in range(len(pois)):
            for j in range(len(pois)):
                ax = fig.add_subplot(gs[i*len(pois) + j])
                # Upper right triangle is disabled
                if j > i:
                    ax.axis('off')
                    # Add legend
                    if i == 0 and j == len(pois)-1:
                        ax.plot(np.inf, np.inf, lw=5, label='truth', c=colors[0])
                        for k, label in enumerate(self.to_compare.keys()):
                            ax.plot(np.inf, np.inf, lw=5, label=label, c=colors[k+1])
                        ax.legend(loc='upper right', handlelength=2, prop={'size': 54})
                        
                # Plot 1D
                elif j == i:              
                    # Plot truth
                    target_plot = truth_singles.requires()[pois[i]]
                    assert isinstance(target_plot, PlotPOIs)
                    target_scan = target_plot.input()
                    assert isinstance(target_scan, law.LocalFileTarget)
                    file = uproot.open(target_scan.path)
                    limit = file['limit']
                    scan_df = pd.DataFrame(limit.arrays(library='pd'))
                    file.close()
                    
                    # Fit deltaNLL to a polynomial
                    scan_df.drop_duplicates(inplace=True)
                    mask = 2*scan_df['deltaNLL'] < 10
                    x = scan_df[pois[i]][mask]
                    y = scan_df['deltaNLL'][mask]
                    p = np.polyfit(x, y, 4)
                    x_fit = np.linspace(x.min(), x.max(), 1000)
                    y_fit = np.polyval(p, x_fit)
                    mask = 2*y_fit < 10
                    
                    # Plot
                    ax.plot(x_fit[mask], 2*y_fit[mask], c=colors[0], lw=5)
                    ax.scatter(scan_df[pois[i]], 2*scan_df['deltaNLL'], c=colors[0], s=100)
                    
                    # Plot models
                    for k, model in enumerate(self.to_compare.keys()):
                        # Load the interpolator
                        interp = self.to_compare[model]['singles']
                        assert isinstance(interp, InterpolateSingles)
                        target = interp.input()[pois[i]]['profile']
                        assert isinstance(target, law.LocalFileTarget)
                        profile = np.load(target.path)
                        mask = profile[1] < 10
                        ax.plot(profile[0][mask], profile[1][mask], c=colors[k+1], lw=5)
                        
                    # Annotate
                    ax.set_ylim((0, 12))
                    ax.set_xlim(truth_singles.bounds[i][0]*1.05, truth_singles.bounds[i][1]*1.05)
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
                    pair = f"{pois[j]},{pois[i]}"
                    target_plot = truth_pairs.input()[pair][2]
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
                    for k, model in enumerate(self.to_compare.keys()):
                        # Load the interpolator
                        interp = self.to_compare[model]['pairs']
                        assert isinstance(interp, InterpolatePairs)
                        target = interp.input()[pair]['profile']
                        assert isinstance(target, law.LocalFileTarget)
                        profile = np.load(target.path)
                        
                        shifts = [2.30, 6.18]
                        for shift, style in zip(shifts, ['-', '--']):
                            ax.contour(profile[0], profile[1], profile[2], 
                                       levels=[shift], colors=colors[k+1], 
                                       linestyles=style, linewidths=5)
                            
                    ax.set_xlim(truth_singles.bounds[j][0]*1.05, truth_singles.bounds[j][1]*1.05)
                    ax.set_ylim(truth_singles.bounds[i][0]*1.05, truth_singles.bounds[i][1]*1.05)
                
                # Label
                if j == 0 and i != 0:
                    ax.set_ylabel(pois[i], fontsize=48)
                else:
                    ax.tick_params(labelleft=False)
                if i == len(pois)-1:
                    ax.set_xlabel(pois[j], fontsize=48)
                else:
                    ax.tick_params(labelbottom=False)
                ax.tick_params(labelsize=40)

        plt.savefig(self.output()['corner'].path, bbox_inches='tight', dpi=125)
    
    def run(self):
        print("Comparing models:")
        for model in self.models_to_compare:
            print(f"  {model}")
        print(f"Against truth model: {self.truth_model}")
        self.make_fishbone()
        self.make_diff1D()
        self.make_corner()
