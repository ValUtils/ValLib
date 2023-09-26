from http.server import ThreadingHTTPServer as HTTPServer
from threading import Thread, Timer
from webbrowser import open as open_url

from .exceptions import HCaptchaTimeoutException
from .handler import CaptchaHandler
from .port import random_port
from .struct import CaptchaSolver


class WebServerSolver(CaptchaSolver):
    _server: HTTPServer
    _address: str
    _port: int = 8080
    _timeout: int
    result: str

    def _init_port(self):
        def set_port():
            self._port = next(random_port())
            self._init_server()
        t = Thread(target=set_port)
        t.start()

    def _init_server(self):
        if hasattr(self, "_server"):
            return
        self._server = HTTPServer((self._address, self._port), CaptchaHandler)

    def __init__(self, address="localhost", timeout=30):
        self._address = address
        self._timeout = timeout
        self._init_port()

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
        self._init_server()
        CaptchaHandler.rqdata = rqdata
        CaptchaHandler.site_key = site_key
        CaptchaHandler.parent = self
        open_url(f"http://{self._address}:{self._port}")
        self._wait()
        self._server.serve_forever()
        if not hasattr(self, "result"):
            raise HCaptchaTimeoutException()
        return self._finish()
