import os, json


def open_json(path: str, default = {}) -> dict:
    """
    Attempts to open a json file and returns its contents as a dict.
    If the file does not exist, a new one will be created with 'default'
    """
    if not os.path.exists(path):
        with open(path, "x"):
            pass
    with open(path, "r") as file:
        content = file.read()
        if content.strip():
            data = json.loads(content)
        else:
            data = default
    file.close()
    return data


def save_json(data: dict, path: str) -> None:
    """Saves a json file"""
    with open(path, "w") as file:
        json.dump(data, file)
    file.close()


