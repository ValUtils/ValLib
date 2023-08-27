class CaptchaSolver:
    result: str

    def token(self, rqdata: str, site_key: str) -> str:
        raise NotImplementedError
