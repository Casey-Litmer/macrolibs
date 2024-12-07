from typing import Any
from .typemacros import tupler
from ._replace_value import _replace_value_recursive, _replace_value_mutable, BREAK_SEARCH
from pickle import loads as pickle_loads, dumps as pickle_dumps




def replace_value_nested(a: list | tuple | dict | set, old_vals: tuple | Any , new_val,
                         callback = None, mode = 'return') -> list | tuple | dict | set | None:
    """
    Replaces a value(s) in a nested data structure.  The value(s) to replace can be of any type,
    including the type of the data structures being searched through.

    Use 'callback' to execute code on replace.
    Callback method should be in the form:  callback(old_val, new_val) -> new_val'
    The return of the method will be the new value.
    ('old_val' will be sampled from any matching value in 'old_vals')

    def callback(old, new):
        print(f"Value {old} replaced with {new}!")
        return new

    Return the BREAK_SEARCH object to end the search:

    def callback(old, new):
        global count
        count += 1
        return new if count <= 10 else BREAK_SEARCH

    Additionally, callback may accept a 'parents' keyword that references a list of all the sequential parents
    that the found value is nested in.
    'parents[0]' is the immediate parent, while 'parent[-1]' is the full structure.

    def callback(old, new, parents):
        global other_value
        if other_value in parents[0]:
            return new
        else:
            return old


    The 'mode' parameter switches between different algorithms:

        - 'return' (default)
            Uses a recursive find and replace algorithm and returns a new data structure without affecting the old one.
            Preserves child types but reinitializes them.  This algorithm is much slower than 'replace' and is subject
            to recursive depth limit.  Accessing 'parents' in the callback will never show updated values.

        - 'replace'
            Replaces the values in the structure and returns None.  Does not search through tuples and will keep
            all dependencies of child types.  Accessing 'parents' in the callback may yield values that have already
            been replaced.

        - 'copy'
            Same as 'replace' but creates a copy of the structure (fast, but high memory usage).  All internal
            dependencies will be conserved, but any pointers to data from outside the structure will not reference
            the cloned data.


    :param a: list, tuple, dict, or set  (all nestings allowed)
    :param old_vals: value(s) to replace
    :param new_val: value to inject
    :param callback: method::old_val -> new_val -> new_val'
    :param mode: switches between different algorithms
    :return: list, tuple, dict, or set
    """

    if mode == 'return':
        return _replace_value_recursive()(a, old_vals, new_val, callback)
    elif mode == 'replace':
        return _replace_value_mutable(a, old_vals, new_val, callback)
    elif mode == 'copy':
        new_a = pickle_loads(pickle_dumps(a))
        _replace_value_mutable(new_a, old_vals, new_val, callback)
        return new_a
    else:
        raise ValueError(f"{mode} is not a valid mode!\nValid modes: ['return', 'replace', 'copy']")



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


