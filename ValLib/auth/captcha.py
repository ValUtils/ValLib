from typing import Any, Dict

from httpx import Client

from ..captcha import solver
from ..debug import Level, log
from ..exceptions import AuthException
from ..structs import User
from ..version import Version


def solve_captcha(data: Dict[str, Any]):
    token = data["captcha"]["hcaptcha"]["data"]
    key = data["captcha"]["hcaptcha"]["key"]
    return solver.token(token, key)


def get_captcha_token(session: Client):
    data = {
        "clientId": "riot-client",
        "language": "",
        "platform": "windows",
        "remember": False,
        "riot_identity": {
            "language": "en_GB",
            "state": "auth",
        },
        "sdkVersion": Version().sdk,
        "type": "auth",
    }
    url = "https://authenticate.riotgames.com/api/v1/login"
    log(Level.DEBUG, f"POST {url}", "network")
    r = session.post(url, json=data)
    response_data = r.json()
    return response_data


def get_login_token(session: Client, user: User, code: str):
    data = {
        "riot_identity": {
            "captcha": f"hcaptcha {code}",
            "language": "en_GB",
            "password": user.password,
            "remember": False,
            "username": user.username
        },
        "type": "auth"
    }
    url = "https://authenticate.riotgames.com/api/v1/login"
    log(Level.DEBUG, f"PUT {url}", "network")
    r = session.put(url, json=data)
    response_data = r.json()
    if response_data["type"] != "success":
        raise AuthException("Wrong password or 2fa")
    return response_data["success"]["login_token"]


def login_cookies(session: Client, login_token: str):
    data = {
        "authentication_type": "RiotAuth",
        "code_verifier": "",
        "login_token": login_token,
        "persist_login": False
    }

    url = "https://auth.riotgames.com/api/v1/login-token"
    log(Level.DEBUG, f"POST {url}", "network")
    session.post(url, json=data)


def captcha_flow(session: Client, user: User):
    captcha_data = get_captcha_token(session)

    captcha_token = solve_captcha(captcha_data)

    login_token = get_login_token(session, user, captcha_token)

    login_cookies(session, login_token)
