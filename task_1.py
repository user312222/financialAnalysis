import yfinance as yf
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import date, timedelta

# Page Configuration
st.set_page_config(page_title="Financial Analysis", page_icon="📈")

# Header Section
st.title("📊 XYZ Financial Analysis")

st.markdown("""
### Unlock Insights Through Data
This application is part of the **Data Visualization and Training** course. 
Explore market trends, historical prices, and volume data for various assets.
""")

# Sidebar Navigation
st.sidebar.title("Filters")
st.sidebar.caption("Your Personal Analyst")

try:
    logo = Image.open("finance.png")
    st.sidebar.image(logo, caption="Filter Options", use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("Logo file not found (finance.png)") 

# Analysis Logic
asset_class = st.sidebar.radio("Asset Class", ["Crypto", "Stock Market"])

if asset_class == "Crypto":
    crypto_select = st.sidebar.selectbox(
        "Select Cryptocurrency",
        ["BTC", "ETH", "XRP", "DOT", "DOGE", "AVAX", "BNB"]
    )
    symbol = f"{crypto_select}-USD"
    currency = "$"

else: 
    stocks = {
        "ASELSAN": "ASELS.IS",
        "THY": "THYAO.IS",
        "GARANTI": "GARAN.IS",
        "AKBANK": "AKBNK.IS",
        "BJK": "BJKAS.IS",
    }
    currency = "₺"

    stock_select = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
    symbol = stocks[stock_select]

# Date Range Selection
days_slider = st.sidebar.select_slider("Select Time Range (Days)", options=range(1, 361), value=30)
today = date.today()

start_date_default = today - timedelta(days=days_slider)

start_date = st.sidebar.date_input("Start Date", value=start_date_default)
end_date = st.sidebar.date_input("End Date", value=today)


def get_metric(latest, high, low, average, currency):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Last Price",
        f"{currency}{latest:.2f}",
        help="The closing price of the most recent selected date."
    )
    col2.metric(
        "Period High",
        f"{currency}{high:.2f}",
        help="The highest price reached within the selected period."
    )
    col3.metric(
        "Period Low",
        f"{currency}{low:.2f}",
        help="The lowest price reached within the selected period."
    )
    col4.metric(
        "Average",
        f"{currency}{average:.2f}",
        help="The average closing price over the selected period."
    )


def get_graph(symbol, start_date, end_date, currency):
    if start_date >= end_date:
        st.error("⚠️ Error: Start date must be before the end date!")
        return

    # Fetching Data
    ticker_data = yf.Ticker(symbol)
    df = ticker_data.history(start=start_date, end=end_date)

    if df.empty:
        st.error(f"No data found for {symbol}. Check the date range or connection.")
        return

    # Renaming for clarity
    df.columns = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]
    
    st.subheader(f"{symbol} Closing Price Chart")

    latest_price = df["Close"].iloc[-1]
    highest_price = df["High"].max()
    lowest_price = df["Low"].min()
    average_price = df["Close"].mean()

    # Display Metrics
    get_metric(latest_price, highest_price, lowest_price, average_price, currency)
    
    # Visualizations
    st.line_chart(df["Close"])
    
    st.subheader("Trading Volume")
    st.line_chart(df["Volume"])
    
    st.subheader("Raw Data")
    st.dataframe(df)


# Execute Function
get_graph(symbol, start_date, end_date, currency)