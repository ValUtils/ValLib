from typing import Any, Dict

from httpx import Client

from ..debug import Level, log
from ..parsing import encode_json, magic_decode
from ..structs import Auth, Token
from ..version import Version

platform = {
    "platformType": "PC",
    "platformOS": "Windows",
    "platformOSVersion": "10.0.22621.1.768.64bit",
    "platformChipset": "Unknown"
}


def make_headers(auth: Auth) -> Dict[str, str]:
    log(Level.VERBOSE, auth)
    return {
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": get_user_agent(),
        "Authorization": f"Bearer {auth.access_token}",
        "X-Riot-Entitlements-JWT": auth.entitlements_token,
        "X-Riot-ClientPlatform": encode_json(platform),
        "X-Riot-ClientVersion": Version().valorant
    }


def post(session: Client, token: Token, url: str) -> Any:
    log(Level.DEBUG, f"POST {url}", "network")
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {token.access_token}",
    }
    r = session.post(url, headers=headers, json={})
    return magic_decode(r.text)


def get_user_agent(app="rso-auth") -> str:
    version = Version().riot
    os = "(Windows;10;;Professional, x64)"
    userAgent = f"RiotClient/{version} {app} {os}"
    log(Level.VERBOSE, userAgent)
    return userAgent
