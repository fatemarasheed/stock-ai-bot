import streamlit as st
import yfinance as yf
import requests
from transformers import pipeline
import sys

# Display Python version for debugging
st.write(f"🧪 Running on Python {sys.version}")

# Load sentiment analysis pipeline
sentiment_model = pipeline("sentiment-analysis")

# Function to fetch news and sentiment
def get_news_sentiment(stock_name):
    api_key = "fe0cfe75051c4aa089949706eac2c2f9"  # 🔁 Replace this with your NewsAPI key
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

# Streamlit UI
st.title("📈 Stock Buy/Sell Suggestion Bot")
stock_name = st.text_input("Enter Stock Name (e.g. Tesla, Apple, Infosys):")

if stock_name:
    # Fetch stock price
    stock = yf.Ticker(stock_name)
    try:
        current_price = stock.history(period="1d")["Close"].iloc[-1]
        st.metric(label="Current Stock Price", value=f"${current_price:.2f}")
    except:
        st.warning("⚠️ Unable to fetch stock price. Please check the stock name.")

    # Fetch news + sentiment
    news_titles, sentiment_scores = get_news_sentiment(stock_name)

    # Display headlines
    st.subheader("📰 News Headlines & Sentiment")
    for title, score in zip(news_titles, sentiment_scores):
        emoji = "✅" if score == "POSITIVE" else "❌" if score == "NEGATIVE" else "➖"
        st.markdown(f"{emoji} **{title}** — *{score}*")

    # Decision Logic
    pos = sentiment_scores.count("POSITIVE")
    neg = sentiment_scores.count("NEGATIVE")

    st.subheader("📊 Suggestion")
    if pos > neg:
        st.success("📈 Suggestion: **BUY**")
    elif neg > pos:
        st.error("📉 Suggestion: **SELL**")
    else:
        st.info("⏸️ Suggestion: **HOLD**")
