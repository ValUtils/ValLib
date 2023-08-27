from importlib_resources import files

from .http import UtilityHandler
from .struct import CaptchaSolver

f = files("ValLib.captcha.assets")
file = f / "captcha.html"
captcha = file.read_text()


class CaptchaHandler(UtilityHandler):
    rqdata: str
    site_key: str
    parent: CaptchaSolver

    def page(self):
        data = captcha.replace("SITE_KEY", self.site_key)
        self.auto_send(data, content_type="text/html")

    def do_rqdata(self):
        self.auto_send(self.rqdata)

    def code(self):
        body = self.read_body()
        if not body or not body.startswith("P1"):
            self.send_error(403)
            return
        self.parent.result = body
        self.auto_send("OK", 200)
        self.server.shutdown()

    def do_GET(self):
        paths = {
            "/": self.page,
            "/v1/hcaptcha/rqdata": self.do_rqdata
        }
        self.routing(paths)

    def do_POST(self):
        paths = {
            "/v1/hcaptcha/response": self.code
        }
        self.routing(paths)
