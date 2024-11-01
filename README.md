```commandline
pip install macrolibs
```

### Macros for type conversions, recursive search, file handling, etc...

-----------
### typemacros

```commandline
import macrolibs.typemacros
```
Includes:
- standardization of **unions**, **intersections**, and **compliments** for all base iterables
- `replace_value_nested` recursive find and replace for all nested data structures
- `maybe_arg` automatic function argument reduction (reductive polymorphism)
- `copy_type` functor with name cache for creating new types (also maps reflexive methods to new type)
- `maybe_type` attempts to apply type constructor
- `wrap_types` attempts to apply type constructor for specified types

*And more!*

-----------

### filemacros

```commandline
import macrolibs.filemacros
```
Includes:
- `get_script_dir` function to return the directory of the call location
  
 (this is different from `os.getcwd` as it will retun the location of the file
  making the function call)
 - `full_walk` returning full paths from `os.walk`

- `open_json` and `save_json` with default format option
