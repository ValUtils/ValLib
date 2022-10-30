import requests
import json

from .riot import make_headers
from .structs import Auth, AuthLoadout
from .parsing import *

def get_api(url, auth: Auth):
	r = requests.get(url, headers=make_headers(auth))
	jsonData = json.loads(r.text)
	return jsonData

def put_api(url, auth: Auth, data):
	req = requests.put(url, headers=make_headers(auth), json=data)
	return req

def get_preference(auth: Auth):
	apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings'
	jsonData = get_api(apiURL, auth)
	if ("data" not in jsonData):
		return {}
	data = zloads(jsonData["data"])
	return data

def set_preference(auth: Auth, data):
	rawData = {
		"type": "Ares.PlayerSettings",
		"data": zdumps(data)
	}
	apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/savePreference'
	req = put_api(apiURL, auth, rawData)
	return req

def get_load_out(loadAuth: AuthLoadout):
	auth = loadAuth.auth
	apiURL = f'https://pd.{loadAuth.region}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout'
	data = get_api(apiURL, auth)
	del data['Subject']
	del data['Version']
	return data

def set_load_out(loadAuth: AuthLoadout, data):
	auth = loadAuth.auth
	apiURL = f'https://pd.{loadAuth.region}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout'
	data = put_api(apiURL, auth, data)
	return data

def get_region(auth: Auth):
	data = {
		"id_token": auth.id_token
	}
	apiURL = 'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant'
	data = put_api(apiURL, auth, data)
	jsonData = json.loads(data.text)
	region = jsonData["affinities"]["live"]
	return region
