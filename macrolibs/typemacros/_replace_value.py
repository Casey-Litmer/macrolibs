from typing import Any, TypeVar
from .typemacros import tupler, maybe_arg


#Custom token to break a search in a callback.
BREAK_SEARCH = object()

Iterables = TypeVar('Iterables', list, tuple, dict, set)

def _replace_value_mutable(a: Iterables, old_vals: tuple | Any, new_val,callback = None) -> Iterables:
    no_callback = callback is None
    callback = callback if callback is not None else lambda old, new, parents: new
    old_vals = tupler(old_vals)

    stack = [(a, [])]  # (current structure, parents)

    # Process the stack iteratively
    while stack:
        #Remove from stack
        current, parents = stack.pop()

        #Replace the current element
        if current in old_vals:
            # (Optimization) Skip maybe_arg for default callback 
            m_callback = callback if no_callback else maybe_arg(callback)
            new_value = m_callback(current, new_val, parents = parents)

            #Break on token
            if new_value is BREAK_SEARCH:
                return a
            
            if parents:
                #Get first parent from list
                parent = parents[0]

                #Update the parent structure with the new value
                if isinstance(parent, list):
                    parent[parent.index(current)] = new_value
                elif isinstance(parent, dict):
                    for k, v in parent.items():
                        if v == current:
                            parent[k] = new_value
                elif isinstance(parent, set):
                    parent.remove(current)
                    parent.add(new_value)
            continue

        #Append Stack for each item in the iterable and join parents list
        if isinstance(current, list):
            stack.extend((item, [current] + parents) for item in current)
        elif isinstance(current, set):
            stack.extend((item, [current] + parents) for item in current)
        elif isinstance(current, dict):
            stack.extend((v, [current] + parents) for v in current.values())

    return a


#The stack based approach is 50% faster and handles deeper recursion, but does not work with tuples.
class _replace_value_recursive():
    def __init__(self):
        self.broken = False

    def __call__(self, a: Iterables, old_vals: tuple | Any, new_val, callback=None, parents=None) -> Iterables:
        #More memory efficient to break early
        if self.broken:
            return a
        
        parents = [] if parents is None else parents # Fix mutable default argument
        initial_callback = callback
        callback = callback if callback is not None else lambda old, new, parents: new
        old_vals = tupler(old_vals)

        if a in old_vals:
            # (Optimization) Skip maybe_arg for default callback 
            m_callback = callback if initial_callback is None else maybe_arg(callback)
            new_value = m_callback(a, new_val, parents = parents)
            if new_value is BREAK_SEARCH:
                self.broken = True
                return a
            else:
                return new_value

        elif isinstance(a, list):
            return type(a)(self(x, old_vals, new_val, initial_callback, [a] + parents) for x in a)
        elif isinstance(a, tuple):
            return type(a)(self(x, old_vals, new_val, initial_callback, [a] + parents) for x in a)
        elif isinstance(a, dict):
            return type(a)({k: self(v, old_vals, new_val, initial_callback, [a] + parents) for k, v in a.items()})
        elif isinstance(a, set):
            return type(a)(self(x, old_vals, new_val, initial_callback, [a] + parents) for x in a)
        else:
            return a