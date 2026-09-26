"""
Authorized demo lab — intentionally misconfigured.

This is a customer-owned-style training target for OSC demos only.
It exposes weak defaults so the Attack→Defend orchestrator can find and fix them.
No exploit payloads; issues are visible via simple HTTP/config inspection.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOST = os.environ.get("LAB_HOST", "127.0.0.1")
PORT = int(os.environ.get("LAB_PORT", "8080"))
SECURE = os.environ.get("LAB_SECURE", "0") == "1"

# Vulnerable defaults (SECURE=0). Hardened when LAB_SECURE=1 after remediation demo.
CONFIG = {
    "app": "osc-demo-payments",
    "env": "staging",
    "debug": not SECURE,
    "cors_allow_origin": "*" if not SECURE else "https://app.example.com",
    "admin_panel_public": not SECURE,
    # Deliberately bad when insecure — orchestrator redacts in artifacts
    "api_key": "sk_live_DEMO_NOT_REAL_12345" if not SECURE else "${API_KEY}",
}


class Handler(BaseHTTPRequestHandler):
    server_version = "OSCLab/0.1"

    def _send(self, code: int, body: dict | str, content_type: str = "application/json"):
        payload = body if isinstance(body, str) else json.dumps(body, indent=2)
        data = payload.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        # Reflects misconfig when insecure
        self.send_header("Access-Control-Allow-Origin", CONFIG["cors_allow_origin"])
        if CONFIG["debug"]:
            self.send_header("X-Debug-Enabled", "true")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[lab] {self.address_string()} {fmt % args}")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path

        if path in ("/", "/health"):
            self._send(200, {"status": "ok", "secure_mode": SECURE, "service": CONFIG["app"]})
            return

        if path == "/debug/config":
            if CONFIG["debug"]:
                # Intentional finding: internal config + secret material exposed
                self._send(200, CONFIG)
            else:
                self._send(404, {"error": "not found"})
            return

        if path == "/admin":
            if CONFIG["admin_panel_public"]:
                self._send(200, {"admin": True, "users": ["alice", "bob"], "note": "no auth in insecure mode"})
            else:
                self._send(401, {"error": "unauthorized"})
            return

        self._send(404, {"error": "not found"})


def main() -> None:
    mode = "SECURE" if SECURE else "INSECURE (demo findings expected)"
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"OSC lab listening on http://{HOST}:{PORT}  mode={mode}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
