import requests

def val_api_version():
	r = requests.get('https://valorant-api.com/v1/version')
	data = r.json()['data']
	val, riot = "", ""
	if ("riotClientVersion" in data):
		val = data["riotClientVersion"]
	if ("riotClientBuild" in data):
		riot = data["riotClientBuild"]
	return val, riot

def val_version():
	get_versions()
	return versions["valorant"]

def riot_version():
	get_versions()
	return versions["riot"]

def get_versions():
	global versions
	if ("versions" in globals()):
		return
	val, riot = val_api_version()
	versions = {
		"valorant": val,
		"riot": riot
	}
