import json
from typing import Any, Optional

import httpx

from .auth import make_headers
from .debug import Level, log
from .structs import Auth


def get(url: str, auth: Auth) -> Any:
    r = simple_get(url, auth)
    jsonData = json.loads(r.text)
    return jsonData


def post(url: str, auth: Auth, data: Optional[Any] = None) -> Any:
    r = simple_post(url, auth, data)
    jsonData = json.loads(r.text)
    return jsonData


def put(url: str, auth: Auth, data: Optional[Any] = None) -> Any:
    r = simple_put(url, auth, data)
    jsonData = json.loads(r.text)
    return jsonData


def delete(url: str, auth: Auth) -> Any:
    r = simple_delete(url, auth)
    jsonData = json.loads(r.text)
    return jsonData


def simple_get(url: str, auth: Auth) -> httpx.Response:
    log(Level.DEBUG, f"GET {url}", "network")
    res = httpx.get(url, headers=make_headers(auth))
    return res


def simple_post(url: str, auth: Auth, data: Optional[Any] = None) -> httpx.Response:
    log(Level.DEBUG, f"POST {url}", "network")
    res = httpx.post(url, headers=make_headers(auth), json=data)
    return res


def simple_put(url: str, auth: Auth, data: Optional[Any] = None) -> httpx.Response:
    log(Level.DEBUG, f"PUT {url}", "network")
    res = httpx.put(url, headers=make_headers(auth), json=data)
    return res


def simple_delete(url: str, auth: Auth) -> httpx.Response:
    log(Level.DEBUG, f"POST {url}", "network")
    res = httpx.post(url, headers=make_headers(auth))
    return res


__all__ = [
    "get", "post", "put", "delete",
    "simple_get", "simple_post", "simple_put", "simple_delete",
]
