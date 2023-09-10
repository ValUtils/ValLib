from http.server import ThreadingHTTPServer as HTTPServer
from threading import Timer
from webbrowser import open as open_url

from .exceptions import HCaptchaTimeoutException
from .handler import CaptchaHandler
from .port import random_port
from .struct import CaptchaSolver


class WebServerSolver(CaptchaSolver):
    _server: HTTPServer
    _address: str
    _port: int
    _timeout: int
    result: str

    def __init__(self, address="localhost", timeout=30):
        port = next(random_port())
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

        #! Careful race condition, easy solve with t.cancel()
        t = Timer(interval=self._timeout,
                  function=self._server.shutdown)
        t.setDaemon(True)
        t.start()
        return t

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
