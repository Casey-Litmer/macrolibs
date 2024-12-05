from typing import Any
from .typemacros import tupler




def replace_value_nested(a: list | tuple | dict | set, old_vals: tuple | Any, new_val,
                         callback=None) -> list | tuple | dict | set:
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
    callback = callback if callback is not None else lambda old, new: new
    old_vals = tupler(old_vals)

    stack = [(a, None)]  # (current structure, parent)
    result = None

    # Process the stack iteratively
    while stack:
        current, parent = stack.pop()

        # If the current element is one of the target values, replace it
        if current in old_vals:
            new_value = callback(current, new_val)

            if parent is not None:
                # Update the parent structure with the new value
                if isinstance(parent, list):
                    parent[parent.index(current)] = new_value
                elif isinstance(parent, tuple):
                    idx = parent.index(current)
                    parent = parent[:idx] + (new_value,) + parent[idx + 1:]
                elif isinstance(parent, dict):
                    for k, v in parent.items():
                        if v == current:
                            parent[k] = new_value
                elif isinstance(parent, set):
                    parent.remove(current)
                    parent.add(new_value)

            continue

        # If the current element is a nested structure, add its elements to the stack
        if isinstance(current, list):
            stack.extend((item, current) for item in current)
        elif isinstance(current, tuple):
            stack.extend((item, current) for item in current)
        elif isinstance(current, set):
            stack.extend((item, current) for item in current)
        elif isinstance(current, dict):
            stack.extend(((k, v), current) for k, v in current.items())

    return result if result else a




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


