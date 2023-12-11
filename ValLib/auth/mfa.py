from httpx import Client

from ..debug import Level, log
from ..mfa import mfa_input
from .validation import validate_login_token


def mfa_auth(session: Client, remember: bool):
    otp = mfa_input.mfa()
    url = "https://authenticate.riotgames.com/api/v1/login"
    log(Level.DEBUG, f"PUT {url}", "network")
    data = {
        "multifactor": {
            "otp": otp,
            "rememberDevice": remember
        },
        "type": "multifactor"
    }
    r = session.put(url, json=data)
    response_data = r.json()
    validate_login_token(response_data)
    return response_data["success"]["login_token"]
