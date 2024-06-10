"""
Makes all profiled 1D and 2D scans
"""

import numpy as np
import pandas as pd
from typing import List
from interpolator.base import rbfInterpolator

def profile1D(interp: rbfInterpolator, poi: str, num: int=50) -> dict:
    """
    Get the 1D profiled scan for the specified POI, using an interpolator
    """    
    # Generate x values
    bounds = interp.bounds[interp.nominal_pois.index(poi)]
    xs = np.linspace(bounds[0], bounds[1], num=num)
    ys = []
    
    # Profile
    free_keys = [key for key in interp.nominal_pois if key != poi]
    for x in xs:
        ys.append(interp.minimize(free_keys, fixed_vals={poi: [x]})['fun'])
    sim_res = interp.minimize(interp.nominal_pois, {})
    interp_min = sim_res['fun']
    interp_min_x = sim_res['x'][interp.nominal_pois.index(poi)]
    
    return {poi: xs, 'deltaNLL': ys, 'best': interp_min, 'best_x': interp_min_x}

def profile2D(interp: rbfInterpolator, pois: List[str], num: int) -> None:
    """
    Get the 2D pairwise profiled scan for the pois specified, \
        using an interpolator
    """

    # Get free keys
    free_keys = [key for key in interp.nominal_pois if key not in pois]
    
    # Get bounds for fixed parameters
    bounds = []
    for poi in pois:
        bounds.append(interp.bounds[interp.nominal_pois.index(poi)])
    
    # Profile
    x = np.linspace(bounds[0][0], bounds[0][1], num)
    y = np.linspace(bounds[1][0], bounds[1][1], num)
    X, Y = np.meshgrid(x, y)
    Z = np.full(X.shape, np.nan).flatten()
    for i, (x, y) in enumerate(zip(X.flatten(), Y.flatten())):
        if len(free_keys) == 0: # TODO re-order lists
            # No profiling to do, just evaluate
            Z[i] = interp.evaluate(pd.DataFrame({poi: [float(val)] for poi, val in zip(pois, [x, y])}))[0]
        else:
            res = interp.minimize(free_keys, fixed_vals={poi: [float(val)] for poi, val in zip(pois, [x, y])})
            Z[i] = res['fun']
    Z = Z.reshape(X.shape)
        
    # Get overall minimum
    sim_res = interp.minimize(interp.nominal_pois, {})
    interp_min = sim_res['fun']
    interp_min_x = sim_res['x'][interp.nominal_pois.index(poi)]
    
    # Save
    return {pois[0]: X, pois[1]: Y, 'deltaNLL': Z, 'best': interp_min, 'best_x': interp_min_x}
