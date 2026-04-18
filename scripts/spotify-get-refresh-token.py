#!/usr/bin/env python3
"""One-shot script to get a Spotify refresh token. Run on your Mac, not the Pi."""

import base64
import http.server
import json
import secrets
import urllib.parse
import urllib.request
import webbrowser

CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "user-read-currently-playing user-read-playback-state user-read-playback-position"

state = secrets.token_hex(8)
auth_url = (
    "https://accounts.spotify.com/authorize?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
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

        creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        req = urllib.request.Request(
            "https://accounts.spotify.com/api/token",
            data=urllib.parse.urlencode({
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            }).encode(),
            headers={
                "Authorization": f"Basic {creds}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        with urllib.request.urlopen(req) as resp:
            tokens = json.loads(resp.read())

        refresh_token = tokens.get("refresh_token")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h2>Done! You can close this tab.</h2>")

    def log_message(self, *args):
        pass

print("Opening Spotify login in your browser...")
webbrowser.open(auth_url)
print("Waiting for callback on http://localhost:8888 ...")

server = http.server.HTTPServer(("localhost", 8888), Handler)
server.handle_request()

if refresh_token:
    print(f"\nRefresh token:\n{refresh_token}\n")
else:
    print("No refresh token received — something went wrong.")
