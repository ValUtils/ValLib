from dataclasses import dataclass, field, is_dataclass
from time import time
from typing import Dict


@dataclass
class User:
    username: str
    password: str

    def __hash__(self):
        return hash(self.username)


class Base:
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if is_dataclass(value):
            self.__dict__.update(value.__dict__)


@dataclass
class Token(Base):
    access_token: str
    id_token: str
    expire: float
    created = time()


@dataclass
class Auth(Token):
    token: Token = field(repr=False)
    entitlements_token: str
    user_id: str
    remember: bool
    cookies: Dict[str, str]
    access_token: str = field(init=False)
    id_token: str = field(init=False)
    expire: float = field(init=False)


@dataclass
class ExtraAuth(Auth):
    username: str
    region: str
    auth: Auth = field(repr=False)
    token: Token = field(init=False)
    user_id: str = field(init=False)
    entitlements_token: str = field(init=False)
    remember: bool = field(init=False)
    cookies: Dict[str, str] = field(init=False)

__all__ = ["User", "Token", "Auth", "ExtraAuth"]
