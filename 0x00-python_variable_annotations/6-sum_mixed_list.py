#!/usr/bin/env python3

"""
Description: type-annotated function sum_mixed_list which takes a list
                mxd_lst of integers and floats.
Parameters: returns their sum as a float.
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ Return sum of list of floats and ints """
    return sum(mxd_lst)
