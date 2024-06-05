"""
Class definitions for interpolators
"""

import os
import pandas as pd
import numpy as np
import numpy.typing as npt
from typing import Any, Dict, List, Tuple
from abc import ABC, abstractmethod
from interpolator.utils import Data
from interpolator.dataSplitter import loadAndSplit
from interpolator.dataLoader import NLLDataset
from interpolator.rbfSplineFast import rbfSplineFast
from scipy.optimize import OptimizeResult, minimize

class Interpolator(ABC):
    """
    Abstract base class for a generic interpolator

    Args:
        ABC (ABC): Helper class for abstract base classes
    """
    @abstractmethod
    def __init__(self) -> None:
        """
        Initialises the Interpolator
        """
        super().__init__()

    @abstractmethod
    def initialise(self, data_config: Data) -> None:
        """
        Loads data and computes weights for the interpolator

        Args:
            data_config (Data): Options for the data
        """
        pass
        
    @abstractmethod
    def evaluate(self, point: Any) -> float:
        """
        Evaluates the interpolator at a specified point

        Args:
            point (Any): The point to evaluate at

        Returns:
            float: The output of the interpolator at that point
        """
        return 0
        
    @abstractmethod
    def minimize(self, free_keys: List[str], 
                 fixed_vals: Dict[str, List[float]]) -> OptimizeResult:
        """
        Minimize the interpolator using SciPy

        Args:
            free_keys (List[str]): The keys to minimise over
            fixed_vals (Dict[str, List[float]]): The fixed values in the fit

        Returns:
            OptimizeResult: The result of optimising
        """
        pass

class rbfInterpolator(Interpolator):
    """
    Interpolates a surface using radial basis functions

    Args:
        Interpolator (Interpolator): The abstract base class
    """
    def __init__(self, data_path: str) -> None:
        """
        Initialises the Interpolator
        """
        super().__init__()
        # self.data_dir = 'data'
        self.data_path = data_path

    def initialise(self, data_config: Data):
        """
        Loads data and computes weights for the interpolator

        Args:
            data_config (Data): Options for the data
        """
        super().initialise(data_config)
        
        self.pois = list(data_config["POIs"].keys())
        self.bounds = [tuple(*val.values()) 
                       for val in data_config["POIs"].values()]
        self.stem = (f"scan.{data_config['channel']}.{data_config['model']}." +
                     f"{data_config['type']}.{data_config['attribute']}.")
            
        # Get a splits as dataframes
        datasets = [] 
        data_train, data_test, best = loadAndSplit(
            self.data_path, data_config, include_best=True,
            split=data_config["fraction"]
            )
        for data in [data_train, data_test]:
            assert isinstance(data.dataset, NLLDataset)
            data_tup = data.dataset[list(data.indices)]
            datasets.append(NLLDataset(*data_tup, data.dataset.POIs))
        # print(f"Best fit point: {best.X, best.Y}")
        datasets[0].append(best)
        self.best = best.X.detach().numpy()[0]
        self.data_train = datasets[0].toFrame()
        self.data_test = datasets[1].toFrame()
        
        # Build interpolator
        self.spline = rbfSplineFast(len(self.data_train.columns)-1)
        eps_range = data_config["interpolator"]["eps_range"]
        rbf_func = "cubic"
        
        # Minimise LOOCV to find best epsilon using scipy
        # print(f'Minimising LOOCV, starting at eps={1.0}, eps in range {eps_range} using {rbf_func} function...')
        r = minimize(self.getLOOCV, x0=[1.], args=(rbf_func,), bounds=eps_range, method='Nelder-Mead')
        
        # Construct best interpolator
        self.spline.initialise(self.data_train, "deltaNLL", radial_func=rbf_func,
                               eps=r['x'][0], rescaleAxis=True)

    def getLOOCV(self, eps: float, rbf_func: str) -> float:
        self.spline.initialise(self.data_train, "deltaNLL", radial_func=rbf_func, 
                               eps=eps, rescaleAxis=True)
        score = self.spline.calculateLOOCV()
        return score
        
    def evaluate(self, point: pd.DataFrame) -> Tuple[float, 
                                                     npt.NDArray[np.float64]]:
        """
        Evaluates the interpolator at a specified point

        Args:
            point (Any): The point to evaluate at

        Returns:
            float: The output of the interpolator at that point
        """
        super().evaluate(point)
        return self.spline.evaluate(point), self.spline.evaluate_grad(point)[0]
    
    def _minimizeWrapper(self, coeffs: List[float], free_keys: List[str],
                         fixed_vals: Dict[str, List[float]],
                         use_grad: bool=True
                         ) -> Tuple[float, npt.NDArray[np.float64]]:
        """
        Handles the passing of parameters from SciPy to the interpolator

        Args:
            coeffs (List[float]): The values of the WCs from SciPy
            free_keys (List[str]): The WCs that are floating in the fit
            fixed_vals (Dict[str, List[float]]): The fixed WC/value pairs
            use_grad (bool, optional): Whether to return the gradient.\
                Defaults to True.

        Returns:
            float: The value of the function at the specified point
        """
        super().minimize(free_keys, fixed_vals)
            
        # Create a blank df
        d = {poi: np.nan for poi in self.pois}
        mask = {poi: False for poi in self.pois}
        
        # Fill in the free values
        for key, coeff in zip(free_keys, coeffs):
            d[key] = coeff
            mask[key] = True
        
        # Fill in the fixed values
        for key, val in fixed_vals.items():
            d[key] = val[0]

        val, grad = self.evaluate(pd.DataFrame([d]))
        
        if use_grad:            
            return val, grad[list(mask.values())]
        else:
            return val
    
    # TODO properly implement gradient calculation (i.e. split self.evaluate)
    def _minimizeWrapperGrad(self, coeffs: List[float], free_keys: List[str],
                             fixed_vals: Dict[str, List[float]],
                             use_grad: bool=True
                            ) -> Tuple[float, npt.NDArray[np.float64]]:
        """
        Handles the passing of parameters from SciPy to the interpolator

        Args:
            coeffs (List[float]): The values of the WCs from SciPy
            free_keys (List[str]): The WCs that are floating in the fit
            fixed_vals (Dict[str, List[float]]): The fixed WC/value pairs
            use_grad (bool, optional): Whether to return the gradient.\
                Defaults to True.

        Returns:
            float: The value of the function at the specified point
        """
        super().minimize(free_keys, fixed_vals)
            
        # Create a blank df
        d = {poi: np.nan for poi in self.pois}
        mask = {poi: False for poi in self.pois}
        
        # Fill in the free values
        for key, coeff in zip(free_keys, coeffs):
            d[key] = coeff
            mask[key] = True
        
        # Fill in the fixed values
        for key, val in fixed_vals.items():
            d[key] = val[0]

        val, grad = self.evaluate(pd.DataFrame([d]))
               
        return grad[list(mask.values())]
    
    def minimize(self, free_keys: List[str], 
                 fixed_vals: Dict[str, List[float]]) -> OptimizeResult:
        """
        Minimize the interpolator using SciPy

        Args:
            free_keys (List[str]): The keys to minimise over
            fixed_vals (Dict[str, List[float]]): The fixed values in the fit

        Returns:
            OptimizeResult: The result of optimising
        """
        super().minimize(free_keys, fixed_vals)
        assert (len(free_keys) + len(fixed_vals)) == len(self.pois)
        
        # Get start point and bounds for free POIs
        start = []
        bounds = []
        for key in free_keys:
            idx = self.pois.index(key)
            start.append(self.best[idx])
            bounds.append(self.bounds[idx])
        
        # Minimize
        use_gradient = True
        res = minimize(self._minimizeWrapper, x0=start, bounds=bounds,
                       jac=use_gradient, args=(free_keys, fixed_vals, use_gradient), 
                       options={'maxls':20, 'disp':-1})
        
        return res
