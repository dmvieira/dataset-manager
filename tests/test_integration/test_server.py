import os
import socketserver
import threading
from http.server import BaseHTTPRequestHandler


class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        filename = os.path.basename(self.path) 
        self.send_response(200)
        self.send_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
        self.end_headers()

        # not sure about this part below
        with open('./tests/resources{}'.format(self.path), 'rb') as _file: 
            self.wfile.write(_file.read())

class TestServer(socketserver.TCPServer):
    allow_reuse_address = True


def server(port=8001):
    httpd = TestServer(("", port), TestHandler)
    httpd_thread = threading.Thread(target=httpd.serve_forever)
    httpd_thread.setDaemon(True)
    httpd_thread.start()
    return httpd