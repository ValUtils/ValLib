from .default import DefaultMfa
from .struct import MfaInput

mfa_input = DefaultMfa()


def set_mfa(new_input: MfaInput):
    global mfa_input
    mfa_input = new_input
