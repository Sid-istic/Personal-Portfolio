import time
import requests
import os
import base64

SPOTIFY_TOKEN_EXPIRES_AT = 0
SPOTIFY_ACCESS_TOKEN = None

def get_spotify_access_token():
    global SPOTIFY_ACCESS_TOKEN, SPOTIFY_TOKEN_EXPIRES_AT
    if SPOTIFY_ACCESS_TOKEN and time.time() < SPOTIFY_TOKEN_EXPIRES_AT:
        return SPOTIFY_ACCESS_TOKEN

    # Get new token
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    resp = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    token_data = resp.json()
    SPOTIFY_ACCESS_TOKEN = token_data["access_token"]
    SPOTIFY_TOKEN_EXPIRES_AT = time.time() + token_data["expires_in"] - 60  # refresh 1 min early
    return SPOTIFY_ACCESS_TOKEN