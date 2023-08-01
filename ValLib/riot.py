import ssl
import time
from typing import Any, Dict, Tuple

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter

from .debug import Level, log
from .exceptions import AuthException
from .parsing import encode_json, magic_decode
from .structs import Auth, Token, User
from .version import Version

platform = {
    "platformType": "PC",
    "platformOS": "Windows",
    "platformOSVersion": "10.0.19045.1.256.64bit",
    "platformChipset": "Unknown"
}

FORCED_CIPHERS = [
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-ECDSA-CHACHA20-POLY1305",
    "ECDHE-RSA-AES128-GCM-SHA256",
    "ECDHE-RSA-CHACHA20-POLY1305",
    "ECDHE+AES128",
    "RSA+AES128",
    "ECDHE+AES256",
    "RSA+AES256",
    "ECDHE+3DES",
    "RSA+3DES"
]


def post(session: Session, token: Token, url: str) -> Any:
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


def get_token(uri: str) -> Token:
    log(Level.VERBOSE, uri)
    access_token = uri.split("access_token=")[1].split("&scope")[0]
    token_id = uri.split("id_token=")[1].split("&")[0]
    expires_in = uri.split("expires_in=")[1].split("&")[0]
    timestamp = time.time() + float(expires_in)
    token = Token(access_token, token_id, timestamp)
    return token


def get_auth_data(response: Response):
    cookies = response.cookies.get_dict()
    data = response.json()
    if "error" in data:
        raise AuthException(data["error"])
    uri = data["response"]["parameters"]["uri"]
    token = get_token(uri)
    return token, cookies


def setup_session() -> Session:
    log(Level.FULL, "Setting up session")

    class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.set_ciphers(":".join(FORCED_CIPHERS))
            kwargs["ssl_context"] = ctx
            return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    session = requests.session()
    session.headers.update({
        "User-Agent": get_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*"
    })
    session.mount("https://", SSLAdapter())
    return session


def setup_auth(session: Session):
    log(Level.EXTRA, "Setting up auth")
    data = {
        "client_id": "riot-client",
        "nonce": "1",
        "redirect_uri": "http://localhost/redirect",
        "response_type": "token id_token",
        "scope": "account openid",
    }

    url = "https://auth.riotgames.com/api/v1/authorization"
    log(Level.DEBUG, f"POST {url}", "network")
    r = session.post(url, json=data)
    return r


def authenticate(user: User, remember=False) -> Auth:
    log(Level.EXTRA, f"Authenticating {user.username}" +
        (' with cookies' if remember else ''))

    session = setup_session()

    setup_auth(session)

    token, cookies = get_auth_token(session, user, remember)

    entitlements_token = get_entitlement(session, token)

    user_id = get_user_info(session, token)

    session.close()

    auth = Auth(token, entitlements_token, user_id, remember, cookies)

    return auth


def cookie_token(cookies: Dict[str, str]):
    log(Level.EXTRA, "Authenticating using cookies")
    session = setup_session()
    session.cookies.update(cookies)
    r = setup_auth(session)
    token, new_cookies = get_auth_data(r)
    return token, new_cookies


def get_auth_token(session: Session, user: User, remember=False) -> Tuple[Token, Dict[str, str]]:
    log(Level.FULL, "Getting auth token")
    data = {
        "type": "auth",
        "username": user.username,
        "password": user.password
    }

    if remember:
        data["remember"] = "true"

    url = "https://auth.riotgames.com/api/v1/authorization"
    log(Level.DEBUG, f"PUT {url}", "network")
    r = session.put(url, json=data)
    token, cookies = get_auth_data(r)
    return token, cookies


def get_entitlement(session: Session, token: Token) -> str:
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


def get_user_info(session: Session, token: Token) -> str:
    log(Level.FULL, "Getting user info")
    data = post(session, token, "https://auth.riotgames.com/userinfo")
    return data["sub"]


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
