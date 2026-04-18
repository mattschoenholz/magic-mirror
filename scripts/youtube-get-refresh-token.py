#!/usr/bin/env python3
"""One-shot script to get a YouTube OAuth refresh token. Run on your Mac, not the Pi."""

import http.server
import json
import secrets
import urllib.parse
import urllib.request
import webbrowser

CLIENT_ID = "YOUR_YOUTUBE_CLIENT_ID"
CLIENT_SECRET = "YOUR_YOUTUBE_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "https://www.googleapis.com/auth/youtube.readonly"

state = secrets.token_hex(8)
auth_url = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    })
)

refresh_token = None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global refresh_token
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        returned_state = params.get("state", [None])[0]

        if returned_state != state or not code:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"State mismatch or missing code.")
            return

        req = urllib.request.Request(
            "https://oauth2.googleapis.com/token",
            data=urllib.parse.urlencode({
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            }).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req) as resp:
            tokens = json.loads(resp.read())

        refresh_token = tokens.get("refresh_token")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h2>Done! You can close this tab.</h2>")

    def log_message(self, *args):
        pass

print("Opening Google login in your browser...")
webbrowser.open(auth_url)
print("Waiting for callback on http://127.0.0.1:8888 ...")

server = http.server.HTTPServer(("127.0.0.1", 8888), Handler)
server.handle_request()

if refresh_token:
    print(f"\nRefresh token:\n{refresh_token}\n")
else:
    print("No refresh token received — check that the OAuth consent screen is configured.")
