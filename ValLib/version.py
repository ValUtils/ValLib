import httpx

from .debug import Level, log
from .exceptions import ValorantAPIError


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Version(metaclass=SingletonMeta):
    valorant: str = ""
    riot: str = ""
    sdk: str = ""

    def fetch_versions(self):
        log(Level.DEBUG, "Fetching versions")
        r = httpx.get("https://valorant-api.com/v1/version")
        if r.is_error:
            raise ValorantAPIError
        data = r.json()["data"]
        return data

    def fetch_sketchy(self):
        log(Level.DEBUG, "Fetching sketchy versions")
        r = httpx.get("https://valorant-api.com/internal/ritoclientversion")
        if r.is_error:
            raise ValorantAPIError
        data = r.json()["data"]
        return data

    def set_sketchy(self):
        data = self.fetch_sketchy()
        try:
            sdk_version = data["riotGamesApiInfo"]["VS_FIXEDFILEINFO"]["FileVersion"]
        except KeyError:
            self.sdk = "23.8.0.1382"
            return
        self.sdk = sdk_version

    def set_versions(self):
        log(Level.FULL, "Setting Riot Versions")
        data = self.fetch_versions()
        if "riotClientVersion" in data:
            self.valorant = data["riotClientVersion"]
            log(Level.DEBUG, "Valorant " + data["riotClientVersion"])
        if "riotClientBuild" in data:
            self.riot = data["riotClientBuild"]
            log(Level.DEBUG, "RiotClient " + data["riotClientBuild"])
        self.set_sketchy()

    def __init__(self):
        if not self.valorant:
            self.set_versions()
