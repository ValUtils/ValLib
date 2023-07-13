from dataclasses import dataclass, field, asdict
from typing import Dict


@dataclass
class User:
    username: str
    password: str


@dataclass
class Token():
    access_token: str
    id_token: str
    expire: float


@dataclass
class Auth(Token):
    token: Token
    entitlements_token: str
    user_id: str
    remember: bool
    cookies: Dict[str, str]
    access_token: str = field(init=False)
    id_token: str = field(init=False)
    expire: float = field(init=False)

    def __post_init__(self):
        super().__init__(**asdict(self.token))


@dataclass
class ExtraAuth(Auth):
    username: str
    region: str
    auth: Auth
    token: str = field(init=False)
    user_id: str = field(init=False)
    entitlements_token: str = field(init=False)
    remember: bool = field(init=False)
    cookies: Dict[str, str] = field(init=False)

    def __post_init__(self):
        super().__init__(**asdict(self.auth))
