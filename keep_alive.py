import threading
import time
import logging
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger(__name__)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def log_message(self, format, *args):
        pass


def _run_health_server(port: int):
    try:
        server = HTTPServer(("0.0.0.0", port), HealthHandler)
        server.serve_forever()
    except Exception as e:
        logger.error(f"Health server error: {e}")


def _ping_loop(url: str, interval: int):
    while True:
        time.sleep(interval)
        try:
            urllib.request.urlopen(url, timeout=10)
            logger.info(f"Keep-alive ping sent to {url}")
        except Exception as e:
            logger.warning(f"Keep-alive ping failed: {e}")


def start_health_server(port: int = 8080):
    thread = threading.Thread(target=_run_health_server, args=(port,), daemon=True)
    thread.start()
    logger.info(f"Health server started on port {port}")


def start_self_ping(url: str, interval_seconds: int = 840):
    thread = threading.Thread(target=_ping_loop, args=(url, interval_seconds), daemon=True)
    thread.start()
    logger.info(f"Self-ping started → {url} every {interval_seconds // 60} min")
