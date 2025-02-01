from fastapi import FastAPI
from fetch_news import fetch_news
from summarize import summarize_text
from sentiment import analyze_sentiment

app = FastAPI()

@app.get("/process")
def process_news(url: str):
    article = fetch_news(url)
    summary = summarize_text(article["text"])
    sentiment = analyze_sentiment(article["text"])
    return {"title": article["title"], "summary": summary, "sentiment": sentiment}