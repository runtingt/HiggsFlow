''' 
Extracts observed and expected values and 1 sigma intervals for a model's POIs.
Also gets their covariance matrix
'''
import os
import json
import uproot
from uproot.models.TH import Model_TH2F_v4, Model_TAxis_v10
import numpy as np
from typing import Dict, List
from collections import defaultdict
from simplified.utils import MAP_HIGGS_PROD_SMEFT

class MuFinder():
    def __init__(self, model, limit_json, model_pois, hesse_path, bins_path, EFT_parametrisation_path, needs_rot=True) -> None:
        # Initial setup
        self.model = model
        self.limit_json = limit_json
        self.model_pois = model_pois
        self.hesse_path = hesse_path
        self.bins_path = bins_path
        self.EFT_parametrisation_path = EFT_parametrisation_path
        self.needs_rot = needs_rot # Whether the model needs rotation (e.g. STXS) or is aready in terms of WCs (e.g. SMEFT)
        self.poi_info = defaultdict(dict)
        self.matchPOIIndex()
        self.corr_poi = np.empty((len(self.poi_info), len(self.poi_info)))
        self.cov_poi = np.empty((len(self.poi_info), len(self.poi_info)))

    def matchPOIIndex(self) -> None:
        """
        Matches the POIs to their indices within the correlation matrix
        """
        # Open file
        with uproot.open(f"{self.hesse_path}") as f:
            corr = f["h_correlation"]
            assert isinstance(corr, Model_TH2F_v4)
            axis = corr.axis(0)
            assert isinstance(axis, Model_TAxis_v10)
            arglist = axis.labels()
            assert isinstance(arglist, list)
        
        # Match POIs to their index in the matrix
        poi_info = defaultdict(dict)
        for poi in self.model_pois:
            poi_info[poi]["index"] = arglist.index(poi)
                
        self.poi_info = poi_info

    def getMuObs(self) -> None:
        """
        Adds the observed value and 1 sigma CI to a dictionary for
        each POI in the model 
        """
        # Open json file
        with open(f"{self.limit_json}") as f:
            data = dict(json.load(f)[self.model])

        # Get the best fit and 1 sigma intervals
        for poi in self.poi_info.keys():
            value = float(data[poi]["Val"])
            lower = float(data[poi]["ErrorLo"])
            upper = float(data[poi]["ErrorHi"])
            
            # Ensure both are nonzero
            if upper == 0 and lower == 0:
                raise ValueError("Hi and lo errors cannot both be zero")
            elif upper == 0:
                print(f"{poi} upper is 0, using lower")
                upper = lower
            elif lower == 0:
                print(f"{poi} lower is 0, using upper")
                lower = upper
            
            # Symmetrise the error
            error = np.mean([np.abs(upper), np.abs(lower)])
            self.poi_info[poi]["obs_val"] = value
            self.poi_info[poi]["obs_err"] = error  

    def getCorrMat(self) -> None:
        """
        Get the correlation matrix for the POIs from the complete matrix
        """
        # Open file
        with uproot.open(f"{self.hesse_path}") as f:
            corr = f["h_correlation"]
            assert isinstance(corr, Model_TH2F_v4)
            
        # Extract covariance matrix of POIs
        for i, ipoi in enumerate(self.poi_info.values()):
            for j, jpoi in enumerate(self.poi_info.values()):
                self.corr_poi[i][j] = corr.values()[ipoi["index"], jpoi["index"]]
        
    def getCovMat(self) -> None:
        """
        Get the covariance matrix for the POIs from the correlation matrix
        """
        # Update correlation matrix
        self.getCorrMat()
        
        # Build covariance matrix
        for i, ipoi in enumerate(self.poi_info.values()):
            sigma_i = ipoi["obs_err"]
            for j, jpoi in enumerate(self.poi_info.values()):
                sigma_j = jpoi["obs_err"]
                self.cov_poi[i][j] = self.corr_poi[i][j]*sigma_i*sigma_j      
    
    def getRotLinearSingle(self, prod: str, dec: str, coeff: str,
                           prod_map: Dict[str, Dict],
                           dec_map: Dict[str, Dict]) -> float:
        
        # Convert from STXS to SMEFT naming
        prod_split = prod.split("_")
        try:
            prod_split[0] = MAP_HIGGS_PROD_SMEFT[prod_split[0]]
        except KeyError:
            prod_split[0] = '_'.join(prod_split[0:2])
            prod_split.pop(1)
            prod_split[0] = MAP_HIGGS_PROD_SMEFT[prod_split[0]]
        prod = '_'.join(prod_split)
        
        # Compute rotation matrix element    
        A_i = prod_map[prod].get('_'.join(['A', coeff]), 0)
        A_f = dec_map[dec].get('_'.join(['A', coeff]), 0)
        A_tot = dec_map['tot'].get('_'.join(['A', coeff]), 0)
                
        return A_i + A_f - A_tot
    
    def getRotQuadSingle(self, prod:str, dec: str, coeffj:str, coeffk:str,
                         prod_map: Dict[str, Dict], 
                         dec_map: Dict[str, Dict]) -> float:
        
        # Convert from STXS to SMEFT naming
        prod_split = prod.split("_")
        try:
            prod_split[0] = MAP_HIGGS_PROD_SMEFT[prod_split[0]]
        except KeyError:
            prod_split[0] = '_'.join(prod_split[0:2])
            prod_split.pop(1)
            prod_split[0] = MAP_HIGGS_PROD_SMEFT[prod_split[0]]
        prod = '_'.join(prod_split)
        
        # Handle squared coefficients
        if coeffj == coeffk:
            coeffj = coeffj + "_2"
            elem_name = '_'.join(['B', coeffj])
        else:
            elem_name = '_'.join(['B', coeffj, coeffk])
        
        # Compute rotation tensor element    
        B_i = prod_map[prod].get(elem_name, 0)
        B_f = dec_map[dec].get(elem_name, 0)
        B_tot = dec_map['tot'].get(elem_name, 0)
        
        return B_i + B_f - B_tot

    def getRotLinear(self, coeff_names: List[str]) -> None:

        # Get values of A from files
        with open(os.path.join(self.EFT_parametrisation_path, 'prod.json')) as f:
            prod_map = dict(json.load(f))
        with open(os.path.join(self.EFT_parametrisation_path, 'decay.json')) as f:
            dec_map = dict(json.load(f))
        
        # Get merged bin definitions
        with open(os.path.join(self.bins_path, 
                               'stxs_stage12_merge.json')) as f:
            merged = dict(json.load(f)['prod_times_dec'])
        
        # Get cross-sections
        with open(os.path.join(self.bins_path, 'stxs_stage12_xs.json')) as f:
            xs = dict(json.load(f))
        
        rot_linear = np.zeros((len(self.poi_info), len(coeff_names)))
        for i, poi in enumerate(self.poi_info):
            prod = poi.split("_XS_")[-1].split("_BR_")[0]
            dec = poi.split("_BR_")[-1]
            
            # Get component bins
            if prod in merged.keys():
                prod_bins = merged[prod]
            else:
                prod_bins = [prod]
                
            # Build the rotation matrix, row by row
            for j, coeff in enumerate(coeff_names):
                bin_entries = []
                bin_xs = []
                for prod_bin in prod_bins:
                    bin_entries.append(self.getRotLinearSingle(prod_bin, dec, coeff, prod_map, dec_map))
                    bin_xs.append(xs[prod_bin])
                rot_linear[i][j] = np.average(bin_entries, weights=bin_xs)
            
        self.rot_linear = rot_linear
        
    def getRotQuad(self, coeff_names: List[str]) -> None:
        # Get values of B from files
        with open(os.path.join(self.EFT_parametrisation_path, 'prod.json')) as f:
            prod_map = dict(json.load(f))
        with open(os.path.join(self.EFT_parametrisation_path, 'decay.json')) as f:
            dec_map = dict(json.load(f))
        
        # Get merged bin definitions
        with open(os.path.join(self.bins_path, 
                               'stxs_stage12_merge.json')) as f:
            merged = dict(json.load(f)['prod_times_dec'])
        
        # Get cross-sections
        with open(os.path.join(self.bins_path, 'stxs_stage12_xs.json')) as f:
            xs = dict(json.load(f))
        
        rot_quad = np.zeros((len(self.poi_info), len(coeff_names), len(coeff_names)))
        for i, poi in enumerate(self.poi_info):
            prod = poi.split("_XS_")[-1].split("_BR_")[0]
            dec = poi.split("_BR_")[-1]
            
            # Get component bins
            if prod in merged.keys():
                prod_bins = merged[prod]
            else:
                prod_bins = [prod]
                
            # Build the rotation tensor by element
            for j, coeffj in enumerate(coeff_names):
                for k, coeffk in enumerate(coeff_names[j:], j): # Symmetric
                    bin_entries = []
                    bin_xs = []
                    for prod_bin in prod_bins:
                        bin_entries.append(self.getRotQuadSingle(prod_bin, dec, coeffj, coeffk,
                                                                 prod_map, dec_map))
                        bin_xs.append(xs[prod_bin])
                    rot_quad[i][j][k] = np.average(bin_entries, weights=bin_xs)
                    rot_quad[i][k][j] = np.average(bin_entries, weights=bin_xs)
            
            self.rot_quad = rot_quad
        
    def getRotMat(self, coeff_names: List[str]) -> None:
        if self.needs_rot:
            self.getRotLinear(coeff_names)
            self.getRotQuad(coeff_names)
        else:
            self.rot_linear = np.eye(len(self.poi_info))
            self.rot_quad = np.zeros((len(self.poi_info), len(coeff_names), len(coeff_names))) # Direct-SMEFT is inherently
        
    def getMuExp(self, coeff_vals: np.ndarray, is_linear: bool=False) -> np.ndarray:
        lin = np.einsum('ij, ...j->...i', self.rot_linear, coeff_vals)
        if is_linear:
            res = 1 + lin
        else:
            quad = np.einsum('ijk, ...j, ...k->...i', self.rot_quad, coeff_vals, coeff_vals)
            res = 1 + lin + quad
        if self.needs_rot:
            return res
        else:
            return res-1
        
if __name__ == "__main__":
    finder = MuFinder()
    
    # Get observed values and 1 sigma CIs
    finder.getMuObs()
    
    # Get correlation matrix
    finder.getCovMat()
    
    # Get expected values at a single point in WC space (for testing)
    finder.getRotMat(["chg", "chw"])
    print(finder.getMuExp(np.array([1, 0])))
    print(finder.getMuExp(np.array([[1, 0], [1,0]])))
