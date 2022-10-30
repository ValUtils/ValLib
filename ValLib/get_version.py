import requests
from time import time
from pathlib import Path
from platform import system
from hachoir.parser import guessParser
from hachoir.metadata import extractMetadata
from hachoir.stream import FileInputStream

from .storage import read_from_drive, save_to_drive, settingsPath

def get_exe_version(path:Path):
	realPath = str(path)
	stream = FileInputStream(realPath)
	parser = guessParser(stream)
	metadata = extractMetadata(parser)
	version = metadata.get("version")
	stream.close()
	return version

def riot_version():
	version = ""
	if (system() == "Windows"):
		version = from_exe()
	if (not version):
		version = fallback()
	return real_version(version)

def fallback():
	versionPath = settingsPath / "riot-version"
	if (not versionPath.exists()):
		return get_save_remote(versionPath)
	modTime = time() - versionPath.stat().st_mtime
	oneWeek = 86400 * 7
	if (modTime > oneWeek):
		return get_save_remote()
	return read_from_drive(versionPath)

def from_exe():
	defaultLocation = Path("C:/Riot Games/Riot Client/RiotClientServices.exe")
	if (not defaultLocation.exists()):
		return
	version = get_exe_version(defaultLocation)
	return version

def from_github_repo():
	api = "https://api.github.com/repos/Morilli/riot-manifests/contents/"
	folder = "Riot Client/KeystoneFoundationLiveWin"
	url = api + folder
	data = requests.get(url).json()
	verData = max(data, key=lambda v: int(v["name"].split(".")[0]))
	version = verData["name"].split("_")[0]
	return version

def get_save_remote(versionPath):
	version = from_github_repo()
	save_to_drive(version, versionPath)
	return version

def real_version(version):
	return f"{version}.{version.split('.')[-1]}"
