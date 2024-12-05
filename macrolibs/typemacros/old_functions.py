from typing import Any
from .typemacros import tupler





#The stack based approach (in searchmacros.py) is 50% faster, vastly more memory efficient,
#and handles deeper recursion.
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
        result = type(a)(replace_value_nested(x, old_vals, new_val, callback) for x in a)
        return result
    elif isinstance(a, tuple):
        return type(a)(replace_value_nested(x, old_vals, new_val, callback) for x in a)
    elif isinstance(a, dict):
        return type(a)({k:replace_value_nested(v, old_vals, new_val, callback) for k,v in a.items()})
    elif isinstance(a, set):
        return type(a)(replace_value_nested(x, old_vals, new_val, callback) for x in a)
    else:
        return a
