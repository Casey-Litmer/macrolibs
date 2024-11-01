from types import GeneratorType
from typing import Any
import inspect


#Unions
#----------------------------------------------------------------------------------------------------------------------

def list_union(A: list | tuple | list[list] | tuple[list], B: list | tuple | None = None) -> list:
    """
    If 'b' is None, the function will perform an iterative union of all lists and tuples in 'a'.
    In this case, 'a' must be a list or tuple of exclusively lists or  tuples.
    Otherwise, perform the union of 'a' and 'b'
    """
    if B is None:
        l_union = list()
        for n in A:
            if isinstance(n, list | tuple):
                l_union = list_union(l_union, n)
            else:
                print("'a' must be a list or tuple of lists or tuples if 'b' is empty")
                raise TypeError
        return l_union
    else:
        return list(A) + list(x for x in B if x not in A)


def tuple_union(A: list | tuple | list[tuple] | tuple[tuple], B: list | tuple | None = None) -> tuple:
    """
    If 'b' is None, the function will perform an iterative union of all lists and tuples in 'a'.
    In this case, 'a' must be a list or tuple of exclusively lists or  tuples.
    Otherwise, perform the union of 'a' and 'b'
    """
    if B is None:
        t_union = tuple()
        for n in A:
            if isinstance(n, list | tuple):
                t_union = tuple_union(t_union, n)
            else:
                print("'a' must be a list or tuple of lists or tuples if 'b' is empty")
                raise TypeError
        return t_union
    else:
        return tuple(A) + tuple(x for x in B if x not in A)


def dict_union(A: dict | list[dict] | tuple[dict], B: dict | None = None) -> dict:
    """
    If 'b' is None, the function will perform an iterative union of all dicts in 'a'.
    In this case, 'a' must be a list or tuple of exclusively dicts.
    Otherwise, perform the union of 'a' and 'b'
    (Leftmost keys have precedence)
    """
    if B is None:
        d_union = dict()
        for n in A:
            if isinstance(n, dict):
                d_union = dict_union(d_union, n)
            else:
                print("'a' must be a list or tuple of dicts if 'b' is empty")
                raise TypeError
        return d_union
    else:
        return dict(A | B)


def set_union(A: set | list[set] | tuple[set], B: set | None = None) -> set:
    """
    If 'b' is None, the function will perform an iterative union of all sets in 'a'.
    In this case, 'a' must be a list or tuple of exclusively sets.
    Otherwise, perform the union of 'a' and 'b'
    """
    if B is None:
        s_union = set()
        for n in A:
            if isinstance(n, set):
                s_union = set_union(s_union, n)
            else:
                print("'a' must be a list or tuple of sets if 'b' is empty")
                raise TypeError
        return s_union
    else:
        return set(A | B)


def type_union(A: list | tuple | dict | set , B: list | tuple | dict | set | None = None) -> list | tuple | dict | set:
    """General union for all types.  A and B must be the same type unless B is None
    In this case, 'A' must be a list or tuple of exclusively sets.
    Otherwise, perform the union of 'a' and 'b'
    """
    if type(A) != type(B) and B is not None:
        print("A and B must be the same type!")
        raise TypeError
    elif isinstance(A, list) and (isinstance(B, list) or B is None):
        return list_union(A, B)
    elif isinstance(A, tuple) and (isinstance(B, tuple) or B is None):
        return tuple_union(A, B)
    elif isinstance(A, dict) and (isinstance(B, dict) or B is None):
        return dict_union(A, B)
    elif isinstance(A, set) and (isinstance(B, set) or B is None):
        return set_union(A, B)


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

def type_compliment(A: list | tuple | dict | set, B: list | tuple | dict | set) -> list | tuple | dict | set:
    """General compliment for all types.  A and B must be the same type"""
    if type(A) != type(B):
        print("A and B must be the same type!")
        raise TypeError
    elif isinstance(A, list) and isinstance(B, list):
        return list_compliment(A, B)
    elif isinstance(A, tuple) and isinstance(B, tuple):
        return tuple_compliment(A, B)
    elif isinstance(A, dict) and isinstance(B, dict):
        return dict_compliment(A, B)
    elif isinstance(A, set) and isinstance(B, set):
        return set_compliment(A, B)


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

def type_intersect(A: list | tuple | dict | set, B: list | tuple | dict | set) -> list | tuple | dict | set:
    """General intersection for all types.  A and B must be the same type"""
    if type(A) != type(B):
        print("A and B must be the same type!")
        raise TypeError
    elif isinstance(A, list) and isinstance(B, list):
        return list_intersect(A, B)
    elif isinstance(A, tuple) and isinstance(B, tuple):
        return tuple_intersect(A, B)
    elif isinstance(A, dict) and isinstance(B, dict):
        return dict_intersect(A, B)
    elif isinstance(A, set) and isinstance(B, set):
        return set_intersect(A, B)


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


def get_attributes(A: type) -> dict:
    """Return a dictionary of name-attribute pairs of a class"""
    return {name:getattr(A,name) for name in dir(A)}



#Functors
#---------------------------------------------------------------------------------------------------------------------

#TODO: UNTESTED! functor mapping of morphisms works for basic types.
class copy_type():
    """
    copy_type(basetype: type, name: str, attributes: dict) -> type

    Create a copy of a type into a new namespace.  If a namespace already exists, it will not create a new type but
    return the already cached type.
    """
    types = [int, float, str, list, tuple, dict, set, frozenset, bool, complex, bytes, bytearray, memoryview, type, object]
    type_cache = {t.__name__:t for t in types}

    def __new__(cls, basetype: type, name: str, attributes: dict = {}) -> type:
        if name not in cls.type_cache:
            #Default __repr__
            new_attributes = {"__repr__":lambda self: f"{name}({basetype(self)})"} | attributes

            #Create new type
            new_type = type(name, (basetype,), new_attributes)

            #Map reflexive morphisms to new type
            def wrap_end_type(f):
                def wrapper(*args, **kwargs):
                    result = f(*args, **kwargs)
                    return maybe_type(new_type, result) if type(result) is basetype else result

                return wrapper

            #Add more to this list if shit starts breaking
            exclude_attrs = (["__class__", "__weakref__", "__ref__", "__repr__", "__init__", "__str__", "__getattr__"]
                             + list(attributes))  #Dont map user defined attributes!

            #setattrs for new_type
            for meth_name in dir(new_type):
                if meth_name not in exclude_attrs and callable(meth_attr := getattr(basetype, meth_name)):
                    setattr(new_type, meth_name, wrap_end_type(meth_attr))

            #Cache type
            cls.type_cache[name] = new_type

        return cls.type_cache[name]


def maybe_type(base_type: type, data: Any) -> type:
    """Attempts to construct a type of 'base_type' with 'data' and returns 'data' if it fails."""
    try:
        return base_type(data)
    except TypeError:
        return data


def wrap_types(wrap: type, data: Any, base_types = ()) -> type:
    """Attempts to apply a type constructor 'wrap' on 'data' if data is/in 'base_types'"""
    if type(base_types) is type:
        base_types = (base_types,)

    if type(data) in base_types:
        return maybe_type(wrap, data)

    else:
        return data
