import yfinance as yf
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import date, timedelta

# Page Configuration
st.set_page_config(page_title="Financial Analysis Dashboard", page_icon="📈", layout="wide")

# Header Section
st.title("📊 Financial Markets Analysis")

st.markdown("""
### Unlock Insights Through Data
This application provides real-time financial data visualization. 
Explore market trends, historical prices, and volume data for various assets.
""")

# Sidebar Navigation
st.sidebar.title("Configuration")
st.sidebar.caption("Market Analysis Tools")

try:
    logo = Image.open("finance.png")
    st.sidebar.image(logo, caption="Settings", use_container_width=True)
except FileNotFoundError:
    st.sidebar.warning("Logo file (finance.png) not found.") 

# Asset Class Selection
asset_class = st.sidebar.radio("Select Asset Class", ["Crypto", "Stock Market"])

if asset_class == "Crypto":
    crypto_select = st.sidebar.selectbox(
        "Choose Cryptocurrency",
        ["BTC", "ETH", "XRP", "DOT", "DOGE", "AVAX", "BNB"]
    )
    symbol = f"{crypto_select}-USD"
    currency_symbol = "$"

else: 
    stocks = {
        "ASELSAN": "ASELS.IS",
        "THY": "THYAO.IS",
        "GARANTI": "GARAN.IS",
        "AKBANK": "AKBNK.IS",
        "BJK": "BJKAS.IS",
    }
    currency_symbol = "₺"
    stock_select = st.sidebar.selectbox("Choose Stock", list(stocks.keys()))
    symbol = stocks[stock_select]

# Date Range Selection
st.sidebar.subheader("Date Selection")
days_slider = st.sidebar.select_slider("Adjust Range (Days)", options=range(1, 361), value=30)
today = date.today()
start_date_default = today - timedelta(days=days_slider)

start_date = st.sidebar.date_input("Start Date", value=start_date_default)
end_date = st.sidebar.date_input("End Date", value=today)

# Functions
def display_metrics(latest, high, low, average, delta, currency):
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric(
        "Last Price",
        f"{currency}{latest:.2f}",
        f"{delta:+.2f}%",
        help="Current price with change since period start"
    )
    m2.metric("Period High", f"{currency}{high:.2f}")
    m3.metric("Period Low", f"{currency}{low:.2f}")
    m4.metric("Average", f"{currency}{average:.2f}")

def get_analysis(symbol, start_date, end_date, currency):
    if start_date >= end_date:
        st.error("⚠️ Error: Start date must be before the end date!")
        return

    # Data Fetching
    ticker_data = yf.Ticker(symbol)
    df = ticker_data.history(start=start_date, end=end_date)

    if df.empty:
        st.error(f"No data available for {symbol}. Please try a different date range.")
        return

    # Standardize column names
    # Note: yfinance returns specific columns, we ensure they are mapped correctly
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    st.divider()
    st.subheader(f"📈 {symbol} Market Overview")

    # Calculation of metrics
    latest_price = df["Close"].iloc[-1]
    highest_price = df["High"].max()
    lowest_price = df["Low"].min()
    average_price = df["Close"].mean()
    first_price = df["Close"].iloc[0]
    
    # Growth/Loss calculation
    performance_delta = ((latest_price - first_price) / first_price) * 100

    # Display Metrics UI
    display_metrics(latest_price, highest_price, lowest_price, average_price, performance_delta, currency)
    
    st.write("") # Spacing

    # Charts
    tab1, tab2, tab3 = st.tabs(["Price Chart", "Volume Analysis", "Raw Data"])
    
    with tab1:
        st.line_chart(df["Close"])
    
    with tab2:
        st.bar_chart(df["Volume"])
        
    with tab3:
        st.dataframe(df, use_container_width=True)

# Run Analysis
get_analysis(symbol, start_date, end_date, currency_symbol)