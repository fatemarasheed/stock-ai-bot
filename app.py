import requests
from transformers import pipeline

# Load sentiment analysis model
sentiment_model = pipeline("sentiment-analysis")

# Define the function
def get_news_sentiment(stock_name):
    api_key = "fe0cfe75051c4aa089949706eac2c2f9"  # Replace with your NewsAPI.org key
    url = f"https://newsapi.org/v2/everything?q={stock_name}&language=en&pageSize=5&sortBy=publishedAt&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()

    news_titles = []
    sentiment_scores = []

    if data.get("status") == "ok" and data.get("articles"):
        for article in data["articles"]:
            title = article["title"]
            news_titles.append(title)

            sentiment = sentiment_model(title)[0]["label"]
            sentiment_scores.append(sentiment)
    else:
        news_titles.append("No news found or error fetching news.")
        sentiment_scores.append("NEUTRAL")

    return news_titles, sentiment_scores
