from http.server import ThreadingHTTPServer as HTTPServer
from webbrowser import open as open_url

from .handler import CaptchaHandler
from .struct import CaptchaSolver


class WebServerSolver(CaptchaSolver):
    _server: HTTPServer
    _address: str
    _port: int
    result: str

    def __init__(self, address="localhost", port=8080):
        self._address = address
        self._port = port
        self._server = HTTPServer((address, port), CaptchaHandler)

    def _finish(self):
        result = self.result
        del self.result
        return result

    def token(self, rqdata: str, site_key: str):
        CaptchaHandler.rqdata = rqdata
        CaptchaHandler.site_key = site_key
        CaptchaHandler.parent = self
        open_url(f"http://{self._address}:{self._port}")
        self._server.serve_forever()
        return self._finish()
