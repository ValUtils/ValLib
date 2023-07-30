import requests

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

    def fetch_versions(self):
        log(Level.DEBUG, "Fetching versions")
        r = requests.get("https://valorant-api.com/v1/version")
        if not r.ok:
            raise ValorantAPIError
        data = r.json()["data"]
        return data

    def set_versions(self):
        log(Level.FULL, "Setting Riot Versions")
        data = self.fetch_versions()
        if "riotClientVersion" in data:
            self.valorant = data["riotClientVersion"]
            log(Level.DEBUG, "Valorant " + data["riotClientVersion"])
        if "riotClientBuild" in data:
            self.riot = data["riotClientBuild"]
            log(Level.DEBUG, "RiotClient " + data["riotClientBuild"])

    def __init__(self):
        if not self.valorant:
            self.set_versions()
