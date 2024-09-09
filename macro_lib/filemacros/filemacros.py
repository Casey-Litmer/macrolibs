import sys, os, inspect


#Script Macros
#----------------------------------------------------------------------------------------------------------------------

def get_script_dir() -> str:
    """Returns the directory of the current script if compiled via pyinstaller or not, ran from anywhere."""
    # Get the stack frame of the caller
    frame = inspect.stack()[1]

    # Get the file path of the caller
    caller_file_path = frame.filename

    # If the caller is a script and not a compiled executable
    if not getattr(sys, 'frozen', False): # Check if the app is not frozen (not compiled with PyInstaller)
        return os.path.dirname(os.path.abspath(caller_file_path))

    # If the caller is a compiled executable
    return os.path.dirname(sys.executable)


#Search Macros
#--------------------------------------------------------------------------------------------------------------------

def full_walk(dir_path: str) -> list:
    """Returns list of full paths from an os.walk"""
    L = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            full_path = os.path.join(root, file)
            L.append(full_path)

    return L