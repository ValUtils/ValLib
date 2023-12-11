from .struct import MfaInput


class DefaultMfa(MfaInput):
    def mfa(self) -> str:
        return input("MFA Code: ")
