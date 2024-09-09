import os, json

#TODO: comments!

def open_json(path: str, default = {}) -> dict:
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
    with open(path, "w") as file:
        json.dump(data, file)
    file.close()


