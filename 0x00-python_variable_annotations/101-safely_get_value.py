#!/usr/bin/env python3

"""
- Description: Augment the following code with the correct duck-typed
                annotations
- Arguments: lst: Sequence[Any]
"""

from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default: Union[T, None] = None)\
        -> Union[Any, T]:
    """
    Return value of key in dict otherwise default

    Args:
        dct (Mapping): input dict
        key (Any): key to lookup in dict
        default (Union[T, None], optional): default value to return if key
                                            does not exist. Defaults to None.

    Returns:
        Union[Any, T]: value of key in dict otherwise default
    """
    if key in dct:
        return dct[key]
    else:
        return default
