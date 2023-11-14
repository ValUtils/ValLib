class AuthException(BaseException):
    pass


class RatelimitException(BaseException):
    pass


class RiotException(BaseException):
    pass


class DecodeException(BaseException):
    pass


class ValorantAPIError(Exception):
    pass
