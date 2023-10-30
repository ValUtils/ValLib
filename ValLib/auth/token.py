import time

from httpx import Client

from ..debug import Level, log
from ..exceptions import AuthException
from ..structs import Token
from .setup import setup_auth


def get_auth_data(session: Client):
    r = setup_auth(session)
    cookies = dict(r.cookies)
    data = r.json()
    if "error" in data:
        raise AuthException(data["error"])
    if "response" not in data:
        msg = "Missing params from auth response, ussually invalid cookies"
        raise AuthException(msg)
    uri = data["response"]["parameters"]["uri"]
    token = get_token(uri)
    return token, cookies


def get_token(uri: str) -> Token:
    log(Level.VERBOSE, uri)
    access_token = uri.split("access_token=")[1].split("&scope")[0]
    token_id = uri.split("id_token=")[1].split("&")[0]
    expires_in = uri.split("expires_in=")[1].split("&")[0]
    timestamp = time.time() + float(expires_in)
    token = Token(access_token, token_id, timestamp)
    return token
