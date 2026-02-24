from pickle import dumps, PicklingError
from types import MethodType


def hashable_repr(obj):
    """Create a recursively hashable representation of any object."""
    if isinstance(obj, (str, int, float, bool, type(None), bytes)):
        return obj
    # Use specific type checks and prepend a type identifier
    elif isinstance(obj, list):
        return ('__list__',) + tuple(hashable_repr(i) for i in obj)
    elif isinstance(obj, tuple):
        return ('__tuple__',) + tuple(hashable_repr(i) for i in obj)
    elif isinstance(obj, dict):
        # Sort items to make dict representation deterministic
        return ('__dict__',) + tuple(sorted(((hashable_repr(k), hashable_repr(v)) for k, v in obj.items()), key=lambda x: str(x[0])))
    elif isinstance(obj, set):
        # Sort elements to make set representation deterministic
        return ('__set__',) + tuple(sorted((hashable_repr(i) for i in obj), key=str))
    elif isinstance(obj, MethodType) or hasattr(obj, '__dict__'):
        return (str(type(obj)), id(obj))
    else:
        # Fallback for other types.
        try:
            # Try to pickle the object. `dumps` returns hashable bytes.
            # We wrap it in a tuple to avoid collision with other types.
            return ('__pickle__', dumps(obj))
        except (PicklingError, TypeError):
            # If it's not pickleable (e.g., a lambda, local function, etc.),
            # fall back to a representation using its id.
            return ('__id__', id(obj))