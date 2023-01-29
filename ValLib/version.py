import requests


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

    def set_versions(self):
        r = requests.get('https://valorant-api.com/v1/version')
        data = r.json()['data']
        if ("riotClientVersion" in data):
            self.valorant = data["riotClientVersion"]
        if ("riotClientBuild" in data):
            self.riot = data["riotClientBuild"]

    def __init__(self):
        if (not self.valorant):
            self.set_versions()
