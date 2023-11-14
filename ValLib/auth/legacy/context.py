"""
https://docs.python.org/3/library/ssl.html#tls-1-3

Thanks floxay
https://github.com/floxay/python-riot-auth
"""
import contextlib
import ctypes
import ssl
import sys
import warnings

CIPHERS13 = ":".join((
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384",
))

CIPHERS = ":".join((
    "ECDHE-ECDSA-CHACHA20-POLY1305",
    "ECDHE-RSA-CHACHA20-POLY1305",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-RSA-AES128-GCM-SHA256",
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES128-SHA",
    "ECDHE-RSA-AES128-SHA",
    "ECDHE-ECDSA-AES256-SHA",
    "ECDHE-RSA-AES256-SHA",
    "AES128-GCM-SHA256",
    "AES256-GCM-SHA384",
    "AES128-SHA",
    "AES256-SHA",
    "DES-CBC3-SHA",  # most likely not available
))

SIGALGS = ":".join((
    "ecdsa_secp256r1_sha256",
    "rsa_pss_rsae_sha256",
    "rsa_pkcs1_sha256",
    "ecdsa_secp384r1_sha384",
    "rsa_pss_rsae_sha384",
    "rsa_pkcs1_sha384",
    "rsa_pss_rsae_sha512",
    "rsa_pkcs1_sha512",
    "rsa_pkcs1_sha1",  # will get ignored and won't be negotiated
))

windll = (
    "libssl-3.dll",
    "libssl-3-x64.dll",
    "libssl-1_1.dll",
    "libssl-1_1-x64.dll",
)


def get_libssl() -> ctypes.CDLL:
    if sys.platform.startswith("win32"):
        for dll_name in windll:
            with contextlib.suppress(FileNotFoundError, OSError):
                return ctypes.CDLL(dll_name)
    if sys.platform.startswith(("linux", "darwin")):
        return ctypes.CDLL(ssl._ssl.__file__)  # type: ignore

    raise NotImplementedError("Failed to load libssl.")


def riot_ssl_ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()

    # https://github.com/python/cpython/issues/88068
    addr = id(ctx) + sys.getsizeof(object())
    ctx_ptr = ctypes.cast(addr, ctypes.POINTER(ctypes.c_void_p)).contents

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        ctx.minimum_version = ssl.TLSVersion.TLSv1  # deprecated since 3.10

    libssl = get_libssl()
    ctx.set_alpn_protocols(["http/1.1"])
    ctx.options |= 1 << 19  # SSL_OP_NO_ENCRYPT_THEN_MAC
    libssl.SSL_CTX_set_ciphersuites(ctx_ptr, CIPHERS13.encode())
    libssl.SSL_CTX_set_cipher_list(ctx_ptr, CIPHERS.encode())
    libssl.SSL_CTX_ctrl(ctx_ptr, 98, 0, SIGALGS.encode())

    return ctx


__all__ = ["riot_ssl_ctx"]
