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
from collections import defaultdict
from tasks.base import ForceableWithNewer
from tasks.interpolation import BuildInterpolator, InterpolateSingles
from tasks.combine import ScanAll, ScanPairs, ScanSingles
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
        # TODO refactor structure
        try:
            self.to_compare = {
                f'interp_{model}' : 
                    {
                        'singles' : InterpolateSingles(**models.models[model].to_params()),
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
        cmap = [0, 2, 1]
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
            ax.scatter(xs+shift, best_fits, s=100, zorder=2, c=colors[cmap[i]])
            
            # Extract the CIs
            for j in range(len(levels)):
                ci = np.array([results[model][poi][f'ci_{j}'] for poi in pois]).T
                ax.plot([xs+shift, xs+shift], ci, c=colors[cmap[i]], 
                        lw=5-2*j, ls=ci_styles[j])
            
            # For a nice legend
            ax.plot(0, lw=10, label=model, c=colors[cmap[i]])
            
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
    
    def run(self):
        print("Comparing models:")
        for model in self.models_to_compare:
            print(f"  {model}")
        print(f"Against truth model: {self.truth_model}")
        self.make_fishbone() # TODO check this still works
        self.make_diff1D()
