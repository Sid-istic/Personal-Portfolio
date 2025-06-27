import os
from flask import jsonify, Blueprint
import requests
from dotenv import load_dotenv
import json

twitter_proxy_bp = Blueprint('twitter_proxy', __name__)

load_dotenv()

USER_ID = "1676973329419501569"
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
USERNAME = os.getenv("TWITTER_USERNAME")
CACHE_FILE = "last_tweets_cache.json"
MAX_TWEETS = 5

@twitter_proxy_bp.route("/latest-tweet")
def latest_tweet():
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results=5&exclude=replies,retweets"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        tweets = resp.json().get("data", [])
        if not tweets:
            raise Exception("No tweets found")
        # Load cache
        cache = []
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        # Add new tweets to cache (avoid duplicates)
        tweet_ids_in_cache = {t["id"] for t in cache}
        for tweet in tweets:
            if tweet["id"] not in tweet_ids_in_cache:
                cache.insert(0, tweet)  # Add new tweet to front
        # Keep only the latest MAX_TWEETS
        cache = cache[:MAX_TWEETS]
        # Save cache
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
        return jsonify(cache)
    except Exception as e:
        # On error, return cached tweets if available
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
            return jsonify(cache)
        return jsonify({"error": str(e)}), 500