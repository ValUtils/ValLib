from typing import Any

from httpx import Response

from .parsing import *
from .request import *
from .structs import Auth, ExtraAuth


def get_preference(auth: Auth) -> Any:
    apiURL = "https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings"
    jsonData = get(apiURL, auth)
    if "data" not in jsonData:
        return {}
    data = zloads(jsonData["data"])
    return data


def set_preference(auth: Auth, data) -> Response:
    rawData = {
        "type": "Ares.PlayerSettings",
        "data": zdumps(data)
    }
    apiURL = "https://playerpreferences.riotgames.com/playerPref/v3/savePreference"
    res = simple_put(apiURL, auth, rawData)
    return res


def get_load_out(auth: ExtraAuth) -> Any:
    apiURL = f"https://pd.{auth.shard}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout"
    data = get(apiURL, auth)
    del data['Subject']
    del data['Version']
    return data


def set_load_out(auth: ExtraAuth, data) -> Response:
    apiURL = f"https://pd.{auth.shard}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout"
    res = simple_put(apiURL, auth, data)
    return res


def get_session(auth: ExtraAuth):
    apiURL = f"https://glz-{auth.region}-1.{auth.shard}.a.pvp.net/session/v1/sessions/{auth.user_id}"
    return get(apiURL, auth.auth)


def get_region(auth: Auth) -> str:
    data = {
        "id_token": auth.id_token
    }
    apiURL = "https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant"
    data = put(apiURL, auth, data)
    region = data["affinities"]["live"]
    return region


def get_shard(region: str) -> str:
    if region in ["latam", "br", "pbe"]:
        return "na"
    return region


def get_extra_auth(auth: Auth, username: str) -> ExtraAuth:
    region = get_region(auth)
    shard = get_shard(region)
    return ExtraAuth(username, region, shard, auth)
