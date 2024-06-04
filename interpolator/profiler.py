"""
Makes all profiled 1D and 2D scans
"""

import numpy as np
from interpolator.base import rbfInterpolator

def profile1D(interp: rbfInterpolator, poi: str, num: int=50) -> dict:
    """
    Get the 1D profiled scan for the specified POI, using an interpolator
    """    
    # Generate x values
    bounds = interp.bounds[interp.pois.index(poi)]
    xs = np.linspace(bounds[0], bounds[1], num=num)
    ys = []
    
    # Profile
    free_keys = [key for key in interp.pois if key != poi]
    for x in xs:
        ys.append(interp.minimize(free_keys, fixed_vals={poi: [x]})['fun'])
    sim_res = interp.minimize(interp.pois, {})
    interp_min = sim_res['fun']
    interp_min_x = sim_res['x'][interp.pois.index(poi)]
    
    return {poi: xs, 'deltaNLL': ys, 'best': interp_min, 'best_x': interp_min_x}