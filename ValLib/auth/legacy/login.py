from httpx import Client

from ...debug import Level, log
from ...structs import Auth, User
from ..info import get_entitlement, get_user_info
from ..setup import setup_auth
from .context import riot_ssl_ctx
from .mfa import extract_auth


def legacy_auth(user: User, remember=False) -> Auth:
    log(Level.EXTRA, f"Authenticating as legacy {user.username}" +
        (' with cookies' if remember else ''))

    session = setup_session()

    setup_auth(session)

    token, cookies = get_auth_data(session, user, remember)

    entitlements_token = get_entitlement(session, token)

    user_id = get_user_info(session, token)

    session.close()

    auth = Auth(token, entitlements_token, user_id, remember, cookies)

    return auth


def get_auth_data(session: Client, user: User, remember: bool):
    log(Level.EXTRA, "Getting legacy auth data")
    body = {
        "language": "en_US",
        "password": user.password,
        "remember": remember,
        "type": "auth",
        "username": user.username
    }
    url = "https://auth.riotgames.com/api/v1/authorization"
    r = session.put(url, json=body)
    token, cookies = extract_auth(session, remember, r)
    return token, cookies


def setup_session() -> Client:
    log(Level.FULL, "Setting up legacy session")
    session = Client(verify=riot_ssl_ctx())
    session.headers.update({
        "User-Agent": "ShooterGame/11 Windows/10.0.22621.1.768.64bit",
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    return session
