import yfinance as yf
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import date, timedelta
import plotly.graph_objects as go
import prophet as ph

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

# Checkbox for Prophet
run_prophet = st.sidebar.checkbox("Enable Prophet Forecasting")

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

def create_price_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines+markers', 
                            name='Close Price', line=dict(color='blue', width=2)))
    fig.update_layout(
        title="Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

def create_volume_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name='Volume', 
                        marker_color='orange'))
    fig.update_layout(
        title="Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

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

    # Charts & Analysis
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Price Chart", "Volume Analysis", "Raw Data", "Advanced Statistics", "Prophet Forecast"])
    
    with tab1:
        create_price_chart(df)
    
    with tab2:
        create_volume_chart(df)
        
    with tab3:
        st.dataframe(df, use_container_width=True)

    with tab4:
        st.subheader("Key Statistics")
        
        # Summary Statistics
        st.write("Summary Statistics:")
        st.dataframe(df.describe(), use_container_width=True)
        
        st.divider()
        
        # Custom Stats
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.write("**Price Metrics**")
            st.metric("Volatility (Std Dev)", f"{df['Close'].std():.2f}")
            st.metric("Median Price", f"{df['Close'].median():.2f}")
            
        with col_stat2:
            st.write("**Volume Metrics**")
            st.metric("Total Volume", f"{df['Volume'].sum():,.0f}")
            max_vol_date = df["Volume"].idxmax().strftime('%Y-%m-%d')
            st.metric("Highest Volume Day", max_vol_date)

        st.divider()

        # Volatility Analysis
        variation_coefficient = df["Close"].std() / df["Close"].mean()
        
        st.subheader("Volatility Assessment")
        st.metric("Variation Coefficient", f"{variation_coefficient:.4f}")
        
        if variation_coefficient < 0.05:
            st.success("🟢 **Low Volatility:** Very stable pricing.")
        elif variation_coefficient < 0.15:
            st.info("🔵 **Moderate Volatility:** Normal market conditions.")
        elif variation_coefficient < 0.30:
            st.warning("🟡 **High Volatility:** Expect price swings.")
        else:
            st.error("🔴 **Extreme Volatility:** High risk asset.")

    with tab5: 
        if run_prophet:
            with st.spinner('Training Prophet model and generating forecast...'):
                fb = df.reset_index()
                fb = fb[["Date", "Close"]]
                fb.columns = ["ds", "y"]
                
                fb['ds'] = fb['ds'].dt.tz_localize(None)
                
                model = ph.Prophet()
                model.fit(fb)
                
                future = model.make_future_dataframe(periods=270)
                predict = model.predict(future)
                
                predict_trend = predict[["ds", "trend"]]
                predict_trend = predict_trend.set_index("ds")
                
                st.subheader("270-Day Trend Forecast")
                st.line_chart(predict_trend["trend"])
        else:
            st.info("👈 Enable 'Prophet Forecasting' in the sidebar to see future predictions.")

# Run Analysis
get_analysis(symbol, start_date, end_date, currency_symbol)
