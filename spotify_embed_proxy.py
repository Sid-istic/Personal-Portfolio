import os
import requests
from flask import jsonify, Blueprint
from dotenv import load_dotenv

from spotify_access_token import get_spotify_access_token  

spotify_embed_proxy_bp = Blueprint('spotify_embed_proxy', __name__)

load_dotenv()

LASTFM_USER = os.getenv("LASTFM_USERNAME")
LASTFM_API_KEY = os.getenv("LastFM_API_KEY")

@spotify_embed_proxy_bp.route('/latest-spotify-embed')
def latest_spotify_embed():
    # 1. Get latest track from Last.fm
    lastfm_url = (
        f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks"
        f"&user={LASTFM_USER}&api_key={LASTFM_API_KEY}&format=json&limit=1"
    )
    lastfm_resp = requests.get(lastfm_url)
    if lastfm_resp.status_code != 200:
        return jsonify({"error": "Could not fetch from Last.fm"}), 500
    data = lastfm_resp.json()
    try:
        track = data["recenttracks"]["track"][0]
        track_name = track["name"]
        artist_name = track["artist"]["#text"]
    except Exception:
        return jsonify({"error": "No recent song found."}), 404

    # 2. Search Spotify for this track
    spotify_search_url = (
        f"https://api.spotify.com/v1/search?q=track:{track_name} artist:{artist_name}&type=track&limit=1"
    )
    headers = {"Authorization": f"Bearer {get_spotify_access_token()}"}
    spotify_resp = requests.get(spotify_search_url, headers=headers)
    if spotify_resp.status_code != 200:
        return jsonify({"error": "Could not fetch from Spotify"}), 500
    spotify_data = spotify_resp.json()
    items = spotify_data.get("tracks", {}).get("items", [])
    if not items:
        return jsonify({"error": "No Spotify track found."}), 404
    track_url = items[0]["external_urls"]["spotify"]

    # 3. Get oEmbed HTML for the track
    oembed_url = f"https://open.spotify.com/oembed?url={track_url}"
    oembed_resp = requests.get(oembed_url)
    if oembed_resp.status_code != 200:
        return jsonify({"error": "Could not fetch oEmbed HTML"}), 500
    oembed_data = oembed_resp.json()

    return jsonify({
        "track_name": track_name,
        "artist_name": artist_name,
        "spotify_url": track_url,
        "embed_html": oembed_data["html"]
    })

