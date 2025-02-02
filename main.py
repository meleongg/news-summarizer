import os
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from newspaper import Article
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer

# Load API key
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

app = FastAPI()

# Load NLP models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = SentimentIntensityAnalyzer()

@app.get("/fetch_news/")
def fetch_news(query: str):
    print("Fetching news")
    """Fetch news articles based on a search phrase"""
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch news")

    articles = response.json().get("articles", [])
    return [{"title": a["title"], "url": a["url"]} for a in articles]

@app.get("/analyze/")
def analyze_article(url: str):
    """Extract, summarize, and analyze sentiment of an article"""
    print("Analyzing url")
    try:
        # Extract article text
        article = Article(url)
        article.download()
        article.parse()
        text = article.text

        # Summarize article (max tokens ~130 words)
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

        # Perform sentiment analysis
        sentiment_score = sentiment_analyzer.polarity_scores(text)["compound"]
        sentiment_label = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"

        return {
            "title": article.title,
            "text": text,
            "summary": summary,
            "sentiment": sentiment_label
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid URL or unable to fetch article")