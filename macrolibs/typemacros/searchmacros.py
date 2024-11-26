from typing import Any
from .typemacros import tupler



def replace_value_nested(a: list | tuple | dict | set, old_vals: tuple | Any , new_val, callback = None) -> list | tuple | dict | set:
    """
    Replaces a value recursively in a data structure.  The value(s) to replace can be of any type,
    including any type of the data structures being searched through.

    Use 'callback' to execute code on replace.
    Callback method should be in the form:  callback(old_val, new_val) -> new_val'
    The return of the method will be the new value.
    ('old_val' will be sampled from any matching value in 'old_vals')

    Example:
    def callback(old, new):
        print(f"Value {old} replaced with {new}!")
        return new

    :param a: list, tuple, dict, or set  (all nestings allowed)
    :param old_vals: value(s) to replace
    :param new_val: value to inject
    :param callback: method::old_val -> new_val -> new_val'
    :return: list, tuple, dict, or set
    """
    callback = callback if callback is not None else lambda old, new:new

    old_vals = tupler(old_vals)

    if a in old_vals:
        return callback(a, new_val)
    elif isinstance(a, list):
        return type(a)(replace_value_nested(x, old_vals, new_val, callback) for x in a)
    elif isinstance(a, tuple):
        return type(a)(replace_value_nested(x, old_vals, new_val, callback) for x in a)
    elif isinstance(a, dict):
        return type(a)({k:replace_value_nested(v, old_vals, new_val, callback) for k,v in a.items()})
    elif isinstance(a, set):
        return type(a)(replace_value_nested(x, old_vals, new_val, callback) for x in a)
    else:
        return callback(a, new_val) if a in old_vals else a


def find_nth(string: str, sub_str: str, n: int, idx = 0) -> int:
    """
    Returns the index of the nth occurance of sub_str in string. (0-based)
    Returns -1 if there is no nth occurance.
    """
    L = len(sub_str)
    index = string.find(sub_str)

    if index != -1:
        if n > 0:
            return find_nth(string[index + L:], sub_str, n - 1, idx + index + L)
        else:
            return idx + index
    else:
        return -1