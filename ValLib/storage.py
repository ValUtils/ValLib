import platform
import json
from pathlib import Path
from os import getenv
from json.decoder import JSONDecodeError


def save_to_drive(data, file):
    f = open(file, "w")
    f.write(data)
    f.close()


def read_from_drive(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data


def json_write(data, file):
    jsonData = json.dumps(data, indent=4)
    save_to_drive(jsonData, file)


def json_read(file):
    try:
        rawData = read_from_drive(file)
        return json.loads(rawData)
    except FileNotFoundError:
        print(f"File not found: {file} at json_read")
    except JSONDecodeError:
        print(f"JSON Decode error in file {file}")
    return {}


def create_path(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def list_dir(dir: Path):
    create_path(dir)
    files = [f.name for f in dir.iterdir() if f.is_file()]
    return files


def linux_path():
    xdg = getenv("XDG_CONFIG_HOME")
    if (xdg):
        return Path(xdg) / "ValUtils"
    return Path().home() / ".ValUtils"


def utils_path():
    global utilsPath
    envPath = getenv("VALUTILS_PATH")
    if (envPath):
        utilsPath = Path(envPath).absolute()
    elif (platform.system() == "Windows"):
        appdata = Path(getenv('APPDATA', "."))
        utilsPath = appdata / "ValUtils"
        create_path(utilsPath)
    elif (platform.system() == "Linux"):
        utilsPath = linux_path()
        create_path(utilsPath)
    return utilsPath


utils_path()
