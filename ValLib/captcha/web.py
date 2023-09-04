from http.server import ThreadingHTTPServer as HTTPServer
from threading import Thread
from time import sleep
from webbrowser import open as open_url

from .exceptions import HCaptchaTimeoutException
from .handler import CaptchaHandler
from .struct import CaptchaSolver


class WebServerSolver(CaptchaSolver):
    _server: HTTPServer
    _address: str
    _port: int
    _timeout: int
    result: str

    def __init__(self, address="localhost", port=8080, timeout=30):
        self._address = address
        self._port = port
        self._timeout = timeout
        self._server = HTTPServer((address, port), CaptchaHandler)

    def _finish(self):
        result = self.result
        del self.result
        return result

    def _wait(self):
        if self._timeout <= 0:
            return

        def timeout():
            sleep(self._timeout)
            self._server.shutdown()

        Thread(target=timeout).start()

    def token(self, rqdata: str, site_key: str):
        CaptchaHandler.rqdata = rqdata
        CaptchaHandler.site_key = site_key
        CaptchaHandler.parent = self
        open_url(f"http://{self._address}:{self._port}")
        self._wait()
        self._server.serve_forever()
        if not hasattr(self, "result"):
            raise HCaptchaTimeoutException()
        return self._finish()
