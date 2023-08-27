from secrets import token_urlsafe

from httpx import Client

from ..debug import Level, log
from .helper import get_user_agent


def setup_session() -> Client:
    log(Level.FULL, "Setting up session")
    session = Client()
    session.headers.update({
        "User-Agent": get_user_agent(),
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    session.cookies.update({
        "tdid": "", "asid": "", "did": "", "clid": ""
    })
    return session


def setup_auth(session: Client):
    log(Level.EXTRA, "Setting up auth")
    data = {
        "client_id": "riot-client",
        "nonce": token_urlsafe(16),
        "redirect_uri": "http://localhost/redirect",
        "response_type": "token id_token",
        "scope": "account openid",
    }

    url = "https://auth.riotgames.com/api/v1/authorization"
    log(Level.DEBUG, f"POST {url}", "network")
    r = session.post(url, json=data)
    return r
