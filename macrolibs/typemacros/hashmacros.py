from pickle import dumps


def hashable_repr(obj):
    """Create a recursively hashable representation of any object."""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple)):
        return tuple(hashable_repr(i) for i in obj)
    elif isinstance(obj, dict):
        return tuple(sorted((hashable_repr(k), hashable_repr(v)) for k, v in obj.items()))
    elif isinstance(obj, set):
        return tuple(sorted(hashable_repr(i) for i in obj))
    elif hasattr(obj, '__dict__'):
        # Class instance: try using __dict__
        return hashable_repr(vars(obj))
    else:
        try:
            dumps(obj)
        except TypeError as e:
            if 'unhashable' in str(e):
                # Fallback: use object identity
                return ('<id>', id(obj))
            else:
                raise e