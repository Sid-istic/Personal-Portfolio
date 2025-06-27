import requests
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
USERNAME = os.getenv("TWITTER_USERNAME")

url = f"https://api.twitter.com/2/users/by/username/{USERNAME}"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
resp = requests.get(url, headers=headers)
print(resp.json())