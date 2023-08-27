from typing import Dict

from ..debug import Level, log
from ..structs import Auth, User
from .captcha import captcha_flow
from .info import get_entitlement, get_user_info
from .setup import setup_auth, setup_session
from .token import get_auth_data


def authenticate(user: User, remember=False) -> Auth:
    log(Level.EXTRA, f"Authenticating {user.username}" +
        (' with cookies' if remember else ''))

    session = setup_session()

    setup_auth(session)

    captcha_flow(session, user)

    token, cookies = get_auth_data(session)

    entitlements_token = get_entitlement(session, token)

    user_id = get_user_info(session, token)

    session.close()

    auth = Auth(token, entitlements_token, user_id, remember, cookies)

    return auth


def cookie_token(cookies: Dict[str, str]):
    log(Level.EXTRA, "Authenticating using cookies")
    session = setup_session()
    session.cookies.update(cookies)
    token, new_cookies = get_auth_data(session)
    return token, new_cookies
