import os
from flask import jsonify, Blueprint
import requests
from dotenv import load_dotenv

twitter_proxy_bp = Blueprint('twitter_proxy', __name__)

load_dotenv()

USER_ID = "1676973329419501569"
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
USERNAME = os.getenv("TWITTER_USERNAME")

@twitter_proxy_bp.route("/latest-tweet")
def latest_tweet():
    try:
        url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results=5&exclude=replies,retweets"
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        tweet = resp.json()["data"][0]
        return jsonify(tweet)
    except Exception as e:
        return jsonify({"error": str(e)}), 500