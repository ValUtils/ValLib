
from typing import Any, Dict

from ..exceptions import *

CATASTROPHIC = "Catastrophic error `{err}` during authentication. Check cookies."
UNKOWN = "Got unknown error `{err}` during authentication."
AUTH = "Failed to authenticate. Make sure username and password are correct. `{err}`."


def validate_auth(data: Dict[str, Any]):
    res_type = data.get("type")
    if res_type == "response":
        return
    if res_type is None:
        RiotException(CATASTROPHIC.format(data))
    err = data.get("error")
    if res_type == "error":
        raise RiotException(UNKOWN.format(err))
    if err == "auth_failure":
        raise AuthException(AUTH.format(err))
    if err == "rate_limited":
        raise RatelimitException()


def validate_login_token(data: Dict[str, Any]):
    res_type = data.get("type")
    if res_type in ["success", "multifactor"]:
        return
    if res_type is None:
        RiotException(CATASTROPHIC.format(data))
    err = data.get("error")
    if res_type == "error":
        raise RiotException(UNKOWN.format(err))
    if err == "rate_limited":
        raise RatelimitException()
