"""
Utilities for handling configurations
"""
from typing import TypedDict, Dict, List, Any
    
class Data(TypedDict):
    """
    Options for the data

    Args:
        TypedDict (TypedDict): Base class for TypedDict
    """
    channel: str
    model: str
    type: str
    attribute: str
    POIs: Dict[str, Dict[str, List[float]]]
    interpolator: Dict[str, Any]
    splitting: str
    fraction: float
    subtractbest: bool
