from httpx import Client, Response

from ...mfa import mfa_input
from ..token import extract_auth as extract


def mfa_auth(session: Client, remember: bool):
    otp = mfa_input.mfa()
    url = "https://auth.riotgames.com/api/v1/authorization"
    data = {
        "code": otp,
        "rememberDevice": remember,
        "type": "multifactor"
    }
    r = session.put(url, json=data)
    return extract(r)


def extract_auth(session: Client, remember: bool, r: Response):
    if r.json()["type"] == "multifactor":
        return mfa_auth(session, remember)
    return extract(r)
