import time

from httpx import Client, Response

from ..debug import Level, log
from ..structs import Token
from .setup import setup_auth
from .validation import validate_auth


def get_auth_data(session: Client):
    r = setup_auth(session)
    token, cookies = extract_auth(r)
    return token, cookies


def extract_auth(r: Response):
    cookies = dict(r.cookies)
    data = r.json()
    validate_auth(data)
    uri = data["response"]["parameters"]["uri"]
    token = get_token(uri)
    return token, cookies


def get_token(uri: str) -> Token:
    log(Level.VERBOSE, uri)
    access_token = uri.split("access_token=")[1].split("&scope")[0]
    token_id = uri.split("id_token=")[1].split("&")[0]
    expires_in = uri.split("expires_in=")[1].split("&")[0]
    timestamp = time.time() + float(expires_in)
    token = Token(access_token, token_id, timestamp, time.time())
    return token
