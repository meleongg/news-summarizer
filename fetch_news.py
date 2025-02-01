import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query="AI policy"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return [{"title": a["title"], "text": a["description"]} for a in articles]