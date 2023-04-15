import requests
import json

from .riot import make_headers
from .structs import Auth, ExtraAuth
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
    if "data" not in jsonData:
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


def get_load_out(auth: ExtraAuth):
    apiURL = f'https://pd.{auth.region}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout'
    data = get_api(apiURL, auth)
    del data['Subject']
    del data['Version']
    return data


def set_load_out(auth: ExtraAuth, data):
    apiURL = f'https://pd.{auth.region}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout'
    data = put_api(apiURL, auth, data)
    return data


def get_session(loadAuth: ExtraAuth):
    region = loadAuth.region
    apiURL = f"https://glz-{region}-1.{region}.a.pvp.net/session/v1/sessions/{loadAuth.user_id}"
    return get_api(apiURL, loadAuth.auth)


def get_region(auth: Auth) -> str:
    data = {
        "id_token": auth.id_token
    }
    apiURL = 'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant'
    data = put_api(apiURL, auth, data)
    jsonData = json.loads(data.text)
    region = jsonData["affinities"]["live"]
    return region
