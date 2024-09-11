from types import GeneratorType
from typing import Any
import inspect


#Unions
#----------------------------------------------------------------------------------------------------------------------

def list_union(a: list | tuple | list[list] | tuple[list], b: list | tuple | None = None) -> list:
    """
    If 'b' is None, the function will perform an iterative union of all lists and tuples in 'a'.
    In this case, 'a' must be a list or tuple of exclusively lists or  tuples.
    Otherwise, perform the union of 'a' and 'b'
    :param a: list or tuple (of lists or tuples)
    :param b: list or tuple
    :return: list
    """
    if b is None:
        l_union = list()
        for n in a:
            if isinstance(n, list | tuple):
                l_union = list_union(l_union, n)
            else:
                print("'a' must be a list or tuple of lists or tuples if 'b' is empty")
                raise TypeError
        return l_union
    else:
        return list(a) + list(x for x in b if x not in a)


def tuple_union(a: list | tuple | list[tuple] | tuple[tuple], b: list | tuple | None = None) -> tuple:
    """
    If 'b' is None, the function will perform an iterative union of all lists and tuples in 'a'.
    In this case, 'a' must be a list or tuple of exclusively lists or  tuples.
    Otherwise, perform the union of 'a' and 'b'
    :param a: list or tuple (of lists or tuples)
    :param b: list or tuple
    :return: tuple
    """
    if b is None:
        t_union = tuple()
        for n in a:
            if isinstance(n, list | tuple):
                t_union = tuple_union(t_union, n)
            else:
                print("'a' must be a list or tuple of lists or tuples if 'b' is empty")
                raise TypeError
        return t_union
    else:
        return tuple(a) + tuple(x for x in b if x not in a)


def dict_union(a: dict | list[dict] | tuple[dict], b: dict | None = None) -> dict:
    """
    If 'b' is None, the function will perform an iterative union of all dicts in 'a'.
    In this case, 'a' must be a list or tuple of exclusively dicts.
    Otherwise, perform the union of 'a' and 'b'
    (Leftmost keys have precedence)
    :param a: dict, list, or tuple (of dicts)
    :param b: set
    :return: dict
    """
    if b is None:
        d_union = dict()
        for n in a:
            if isinstance(n, dict):
                d_union = dict_union(d_union, n)
            else:
                print("'a' must be a list or tuple of dicts if 'b' is empty")
                raise TypeError
        return d_union
    else:
        return dict(a | b)


def set_union(a: set | list[set] | tuple[set], b: set | None = None) -> set:
    """
    If 'b' is None, the function will perform an iterative union of all sets in 'a'.
    In this case, 'a' must be a list or tuple of exclusively sets.
    Otherwise, perform the union of 'a' and 'b'
    :param a: set, list, or tuple (of dicts)
    :param b: set
    :return: set
    """
    if b is None:
        s_union = set()
        for n in a:
            if isinstance(n, set):
                s_union = set_union(s_union, n)
            else:
                print("'a' must be a list or tuple of sets if 'b' is empty")
                raise TypeError
        return s_union
    else:
        return set(a | b)


#Compliments
#-------------------------------------------------------------------------------------------------------------------

def list_compliment(A: list, B: list) -> list:
    """Returns a list containing all items in A that are not in B"""
    return list(a for a in A if a not in B)

def tuple_compliment(A: tuple, B: tuple) -> tuple:
    """Returns a tuple containing all items in A that are not in B"""
    return tuple(a for a in A if a not in B)

def dict_compliment(A: dict, B: dict, match_vals= False) -> dict:
    """Returns a dict containing all keys in A that are not in B"""
    return dict({key:val for key, val in A.items() if (key, val) not in B.items()}) if match_vals else \
        dict({key:A[key] for key in A if key not in B})

def set_compliment(A: set, B: set) -> set:
    """Returns a set containing all members in A that are not in B"""
    return set(a for a in A if a not in B)


#Intersections
#---------------------------------------------------------------------------------------------------------------------

def list_intersect(A: list, B: list) -> list:
    """Returns a list returning all items in A that are also in B"""
    return list(a for a in A if a in B)

def tuple_intersect(A: tuple, B: tuple) -> tuple:
    """Returns a list returning all items in A that are also in B"""
    return tuple(a for a in A if a in B)

def dict_intersect(A: dict, B: dict, match_vals= False) -> dict:
    """Returns a dict returning all items (keys:vals) in A that are also in B if match_vals is True
    else, only compares keys"""
    return dict({key:val for key, val in A.items() if (key, val) in B.items()}) if match_vals else \
        dict({key:A[key] for key in A if key in B})

def set_intersect(A: set, B: set) -> set:
    """Returns a set returning all members in A that are also in B"""
    return set(a for a in A if a in B)


#Syntax Converters
#----------------------------------------------------------------------------------------------------------------------

def tupler(a: tuple | Any) -> tuple:
    """
    Passes tuples and generator objects to tuples, and parenthesizes anything else.
    This effectively bypasses the need for a comma in defining a singleton tuple;  (a) -> (a,)
    """
    if isinstance(a, tuple | GeneratorType):
        return tuple(a)
    else:
        return (a,)


#Expansions
#----------------------------------------------------------------------------------------------------------------------

def replace_value_nested(a: list | tuple | dict | set, old_vals: tuple | Any , new_val) -> list | tuple | dict | set:
    """
    Replaces a value recursively in a data structure.  The value(s) to replace can be of any type,
    including any type of the data structures being searched through.
    :param a: list, tuple, dict, or set  (all nestings allowed)
    :param old_vals: value(s) to replace
    :param new_val: value to inject
    :return: list, tuple, dict, or set
    """
    old_vals = tupler(old_vals)

    if a in old_vals:
        return new_val
    elif isinstance(a, list):
        return type(a)(replace_value_nested(x, old_vals, new_val) for x in a)
    elif isinstance(a, tuple):
        return type(a)(replace_value_nested(x, old_vals, new_val) for x in a)
    elif isinstance(a, dict):
        return type(a)({k:replace_value_nested(v, old_vals, new_val) for k,v in a.items()})
    elif isinstance(a, set):
        return type(a)(replace_value_nested(x, old_vals, new_val) for x in a)
    else:
        return new_val if a in old_vals else a



#Function Macros
#----------------------------------------------------------------------------------------------------------------------

def maybe_arg(func, pass_to_kwargs= False):
    """
    Usage: maybe_arg(func)(*args, **kwargs)        Reductive polymorphism.

    Modifies "func" to take an arbitrary number of args and kwargs but discards them (right to left) if "func"
    recieves too many.  Likewise, if a keyword argument not present in "func", it will be ignored.

    For example:
    def f(x, y, z=0)
    maybe_arg(f)(1,2,3) -> f(1,2)  #f ignores 3 because x and y are already satisfied.

    By default, any keyword argument will not accept positional arguments.  This can be changed with the
    "pass_to_kwargs" tag.  If set to True, positional arguments with a default value will also be filled.*

    *All positional kwargs will be overwritten by manually running with kwargs.
    """
    POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD
    EMPTY = inspect.Parameter.empty
    VAR_POSITIONAL = inspect.Parameter.VAR_POSITIONAL

    params = inspect.signature(func).parameters.items()
    required_pars = tuple(par for _, par in params
                          if par.kind in (POSITIONAL_OR_KEYWORD, VAR_POSITIONAL) and par.default is EMPTY)

    def wrapper(*args, **kwargs):
        args = args if pass_to_kwargs or not required_pars or required_pars[-1].kind is VAR_POSITIONAL \
            else args[:len(required_pars)]
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            s = str(e)
            if "positional argument" in s or "multiple values " in s:
                return wrapper(*args[:-1], **kwargs)
            elif "keyword argument '" in s:
                pos = s.index("keyword argument '") + 18
                k = s[pos:][:s[pos:].index("\'")]
                return wrapper(*args, **dict_compliment(kwargs,{k:kwargs[k]}))
            else:
                raise e

    return wrapper