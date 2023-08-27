from httpx import Client

from ..debug import Level, log
from ..parsing import magic_decode
from ..structs import Token
from .helper import get_user_agent, post


def get_entitlement(session: Client, token: Token) -> str:
    log(Level.FULL, "Getting entitlement token")

    url = "https://entitlements.auth.riotgames.com/api/token/v1"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {token.access_token}",
        "User-Agent": get_user_agent("entitlements"),
    }

    r = session.post(url, headers=headers, json={})
    data = magic_decode(r.text)
    return data["entitlements_token"]


def get_user_info(session: Client, token: Token) -> str:
    log(Level.FULL, "Getting user info")
    data = post(session, token, "https://auth.riotgames.com/userinfo")
    return data["sub"]
