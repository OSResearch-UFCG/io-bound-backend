import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", "8080"))
DEFAULT_MB = 50
CHUNK_SIZE = 1024 * 1024


def write_and_read_file(size_mb):
    chunk = os.urandom(CHUNK_SIZE)
    path = os.path.join(tempfile.gettempdir(), f"io-bound-{os.getpid()}.bin")

    with open(path, "wb") as file:
        for _ in range(size_mb):
            file.write(chunk)
        file.flush()
        # Sem fsync os dados ficam no page cache e o disco nem é tocado.
        os.fsync(file.fileno())

    bytes_read = 0
    with open(path, "rb") as file:
        while True:
            data = file.read(CHUNK_SIZE)
            if not data:
                break
            bytes_read += len(data)

    os.remove(path)
    return bytes_read


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        mb = int(query.get("mb", [DEFAULT_MB])[0])

        bytes_read = write_and_read_file(mb)

        body = json.dumps({"mb": mb, "bytes_read": bytes_read}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


print(f"io-bound-backend ouvindo na porta {PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
