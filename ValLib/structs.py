from dataclasses import dataclass, field
from typing import Dict


@dataclass
class User:
    username: str
    password: str


@dataclass
class Auth:
    access_token: str
    id_token: str
    entitlements_token: str
    user_id: str
    cookies: Dict[str, str]


@dataclass
class ExtraAuth(Auth):
    username: str
    region: str
    auth: Auth
    user_id: str = field(init=False)
    id_token: str = field(init=False)
    access_token: str = field(init=False)
    entitlements_token: str = field(init=False)
    cookies: Dict[str, str] = field(init=False)

    def __post_init__(self):
        if not self.auth:
            return
        self.user_id = self.auth.user_id
        self.id_token = self.auth.id_token
        self.access_token = self.auth.access_token
        self.entitlements_token = self.auth.entitlements_token
        self.cookies = self.auth.cookies
