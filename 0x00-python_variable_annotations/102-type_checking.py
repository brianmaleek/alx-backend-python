#!/usr/bin/env python3

"""
- Description: Augment the following code with the correct duck-typed
                annotations
- Arguments: lst: Sequence[Any]
"""

from typing import Tuple, List, Any, Sequence


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Zoom an array

    Args:
        lst (Tuple): Tuple to zoom
        factor (int, optional): Zoom factor. Defaults to 2.

    Returns:
        List: Zoomed list
    """
    zoomed_in: List = ([
        item for item in lst
        for item in range(factor)
    ])
    return zoomed_in


array: Tuple = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
