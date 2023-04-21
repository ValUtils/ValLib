import json
import jwt
import base64
import zlib

from typing import Any

from .exceptions import DecodeException


def encode_json(data: Any) -> str:
    str = json.dumps(data).encode("utf-8")
    return base64.b64encode(str).decode("utf-8")


def decode_json(data: str) -> Any:
    str = base64.b64decode(data.encode("utf-8"))
    return json.loads(str)


def magic_decode(string: str) -> Any:
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
    return json.loads(inflated_data)


def zdumps(data: Any) -> str:
    stringify = json.dumps(data).encode("utf-8")
    return zencode(stringify).decode("utf-8")
