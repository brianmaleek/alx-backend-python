#!/usr/bin/env python3

"""
- Description: Augment the following code with the correct
                duck-typed annotations
- Arguments: lst: Sequence[Any]
"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Return first element of list otherwise None

    Args:
        lst (Sequence[Any]): input sequence

    Returns:
        Union[Any, None]: first element of list otherwise None
    """
    if lst:
        return lst[0]
    else:
        return None
