import re
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy.optimize import OptimizeResult, minimize
from simplified.getSignalStrengths import MuFinder
from interpolator.base import Interpolator
from law.logger import get_logger
logger = get_logger('luigi-interface')

class SimplifedInterpolator(Interpolator):
    """
    Constructs a simplified approximation using the chi2 defined as (mu(c)-mu_obs)^T * inv_cov * (mu(c)-mu_obs)
    """
    def __init__(self, pois, bounds, is_linear, mu_opts):
        self.is_linear = is_linear
        
        # Strip the POIs
        self.nominal_pois = pois
        if self.is_linear:
            pois = [poi[1:] for poi in pois]
        self.pois = [re.sub("XE\d+", "", poi) for poi in pois]
        self.scalings = np.zeros(len(self.pois))
        for i, poi in enumerate(pois):
            match = re.search(r"(?<=XE)\d+", poi)
            if match:
                digits = int(match.group(0))
            else:
                digits = 0
            self.scalings[i] = 10**digits
        self.bounds = bounds
            
        self.initialise(mu_opts)

    def initialise(self, data_config) -> None:
        # Extract the matrices from the impacts
        self.finder = MuFinder(**data_config)
        if not self.finder.needs_rot:
            self.scalings = np.ones(len(self.pois))
        self.finder.getMuObs()
        self.finder.getCovMat()
        self.finder.getRotMat(self.pois)
        
        # Extract observed values and their covariance 
        self.mu_obs = np.array([val['obs_val'] for val in self.finder.poi_info.values()]).astype(float)
        self.cov_mat = self.finder.cov_poi
        self.inv_cov_mat = np.linalg.inv(self.cov_mat)
        
        # Get the best fit value
        self.min = 0
        self.min_x = np.zeros(len(self.pois))
        self.min_res = self.minimize(free_keys=self.nominal_pois, fixed_vals={})
        if self.min_res['success']:
            self.min = self.min_res['fun']
            self.min_x = self.min_res['x']
        else:
            raise RuntimeError("Failed to find minimum chi-squared value.")
        logger.info(f"Found minimum chi2 value: {self.min} at {self.min_x}")
        
    def evaluate(self, point) -> float:
        super().evaluate(point)
        poi_values = np.array(point[self.nominal_pois])
        if len(poi_values.shape) == 1:
            poi_values = poi_values.reshape(1, -1)
        
        # Handle any power of 10 scaling
        poi_values /= self.scalings
        
        # Get the expected values
        mu_exp = self.finder.getMuExp(poi_values, self.is_linear)
        
        # Calculate the chi2, but return *half* the value to approximate NLL
        diff = self.mu_obs - mu_exp
        return 0.5*(np.diag(diff @ self.inv_cov_mat @ diff.T) - self.min)
    
    def getPoint(self, coeffs: List[float], free_keys: List[str],
                 fixed_vals: Dict[str, List[float]]
                 ) -> Tuple[Dict[str, float], Dict[str, bool]]:

        # Create a blank df
        d = {poi: np.nan for poi in self.nominal_pois}
        mask = {poi: False for poi in self.nominal_pois}
        
        # Fill in the free values
        for key, coeff in zip(free_keys, coeffs):
            d[key] = coeff
            mask[key] = True
        
        # Fill in the fixed values
        for key, val in fixed_vals.items():
            d[key] = val[0]
            
        return d, mask
    
    def _minimizeWrapper(self, coeffs: List[float], free_keys: List[str],
                         fixed_vals: Dict[str, List[float]]) -> float:
        d, _ = self.getPoint(coeffs, free_keys, fixed_vals)
        chi2 = self.evaluate(pd.DataFrame([d]))
        return chi2[0]
    
    def minimize(self, free_keys: List[str], fixed_vals: Dict[str, List[float]]) -> OptimizeResult:
        super().minimize(free_keys, fixed_vals)
        start = [self.min_x[self.nominal_pois.index(key)] for key in free_keys]
        
        if len(free_keys) == 0:
            d, _ = self.getPoint(list(fixed_vals.values()), [], fixed_vals)
            chi2 = self.evaluate(pd.DataFrame([d]))[0]
            return OptimizeResult({'fun': chi2, 'x': list(fixed_vals.values()), 
                                   'success': True, 'message': 'Fixed values provided.'})

        res = minimize(self._minimizeWrapper, x0=start, args=(free_keys, fixed_vals), method='L-BFGS-B')
        return res

class Approximator():
    """
    Configuration for approximate models, defines what impacts model to use.
    """
    def __init__(self, model: str, needs_rot: bool):
        self.model = model
        self.needs_rot = needs_rot
        
    def to_params(self):
        return {
            "model": self.model,
        }
