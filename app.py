import sys
st.write(f"🧪 Running on Python {sys.version}")
import streamlit as st
import yfinance as yf
import requests
from transformers import pipeline

# --- Initialize sentiment model
sentiment_model = pipeline("sentiment-analysis")

# --- News API Key (paste your key here)
API_KEY = "YOUR_NEWSAPI_KEY"

# --- Function: Get stock price
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")
    price = stock.info.get("currentPrice", "N/A")
    return price, hist

# --- Function: Get news headlines
def get_news_about_stock(ticker, api_key):
    url = f"https://newsapi.org/v2/everything?q={ticker} stock&language=en&sortBy=publishedAt&pageSize=5&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return [a["title"] for a in data.get("articles", [])]

# --- Function: Analyze sentiment
def analyze_sentiment(headlines):
    results = sentiment_model(headlines)
    return [r['label'] for r in results]

# --- Function: Final decision
def suggest_action(ticker, api_key):
    price, hist = get_stock_info(ticker)
    headlines = get_news_about_stock(ticker, api_key)
    sentiments = analyze_sentiment(headlines)

    pos = sentiments.count("POSITIVE")
    neg = sentiments.count("NEGATIVE")

    if pos > neg:
        suggestion = "BUY 📈"
    elif neg > pos:
        suggestion = "SELL 📉"
    else:
        suggestion = "HOLD 🤝"

    return price, headlines, sentiments, suggestion

# --- Streamlit UI
st.title("📊 Stock Buy/Sell Suggestion Bot")
ticker_input = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, INFY)")

if ticker_input:
    with st.spinner("Analyzing..."):
        try:
            price, headlines, sentiments, suggestion = suggest_action(ticker_input.upper(), API_KEY)

            st.markdown(f"### 📌 Current Price: **${price}**")
            st.markdown("### 📰 News Headlines & Sentiment:")
            for h, s in zip(headlines, sentiments):
                st.write(f"- {h} → **{s}**")

            st.markdown(f"### ✅ Final Suggestion: **{suggestion}**")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
