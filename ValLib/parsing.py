import base64
import json
import zlib
from reprlib import aRepr
from typing import Any

import jwt

from .debug import Level, log
from .exceptions import DecodeException


def encode_json(data: Any) -> str:
    log(Level.VERBOSE, aRepr.repr(data))
    str = json.dumps(data).encode("utf-8")
    return base64.b64encode(str).decode("utf-8")


def decode_json(data: str) -> Any:
    str = base64.b64decode(data.encode("utf-8"))
    data = json.loads(str)
    log(Level.VERBOSE, aRepr.repr(data))
    return data


def magic_decode(string: str) -> Any:
    log(Level.VERBOSE, string)
    try:
        return json.loads(string)
    except json.JSONDecodeError:
        pass
    try:
        return jwt.decode(string, options={"verify_signature": False})
    except jwt.exceptions.DecodeError:
        pass
    raise DecodeException


def zdecode(b64string: str) -> bytes:
    decoded_data = base64.b64decode(b64string)
    return zlib.decompress(decoded_data, -15)


def zencode(string_val: bytes) -> bytes:
    zlibbed_str = zlib.compress(string_val)
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string)


def zloads(b64string: str) -> Any:
    inflated_data = zdecode(b64string)
    data = json.loads(inflated_data)
    log(Level.VERBOSE, aRepr.repr(data))
    return data


def zdumps(data: Any) -> str:
    log(Level.VERBOSE, aRepr.repr(data))
    stringify = json.dumps(data).encode("utf-8")
    return zencode(stringify).decode("utf-8")


__all__ = [
    "encode_json", "decode_json",
    "zdecode", "zencode",
    "zloads", "zdumps",
    "magic_decode"
]
