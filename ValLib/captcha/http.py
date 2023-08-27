from http.server import BaseHTTPRequestHandler
from typing import Callable, Dict
from urllib.parse import urlparse


class UtilityHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def auto_send(self, data, status=200, content_type="text/plain"):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)
        self.wfile.flush()

    def routing(self, paths: Dict[str, Callable]):
        url = urlparse(self.path).path
        if url not in paths:
            self.send_error(404, "Not here")
            return
        paths[url]()

    def read_body(self):
        try:
            content_length = int(self.headers['Content-Length'])
            return self.rfile.read(content_length).decode('utf-8')
        except:
            return None
