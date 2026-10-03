import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from app.handler import lambda_handler


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/shorten":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        event = {
            "httpMethod": "POST",
            "body": body,
        }

        self.handle_lambda(event)

    def do_GET(self):
        parsed = urlparse(self.path)
        code = parsed.path.lstrip("/")

        event = {
            "httpMethod": "GET",
            "pathParameters": {
                "code": code,
            },
        }

        self.handle_lambda(event)

    def handle_lambda(self, event):
        result = lambda_handler(event, None)

        self.send_response(result["statusCode"])

        for name, value in result.get("headers", {}).items():
            self.send_header(name, value)

        body = result.get("body", "").encode("utf-8")

        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), RequestHandler)

    print("URL shortener running on http://localhost:8080")

    server.serve_forever()
