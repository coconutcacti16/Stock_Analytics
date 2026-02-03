import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
# Page Configuration
st.set_page_config(
    page_title="Stock Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for "Yahoo Finance" look
st.markdown("""
<style>
    .metric-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 14px;
        color: #5b6b79;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 600;
        color: #1d1d1f;
    }
    /* Hide Streamlit default styling elements if needed to look cleaner */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
def format_number(num):
    if num is None:
        return "N/A"
    if num >= 1_000_000_000_000:
        return f"{num/1_000_000_000_000:.2f}T"
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    if num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    return f"{num:.2f}"
def main():
    # Sidebar
    st.sidebar.title("Stock Search")
    ticker = st.sidebar.text_input("Enter Ticker Symbol", value="AAPL").upper()
    
    # Time period selection
    period_options = {
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "YTD": "ytd",
        "1Y": "1y",
        "2Y": "2y",
        "5Y": "5y",
        "MAX": "max"
    }
    selected_period = st.sidebar.selectbox("Period", list(period_options.keys()), index=4) # Default 1Y
    if ticker:
        stock = yf.Ticker(ticker)
        
        # 1. Try to get history first (Critical)
        try:
            history = stock.history(period=period_options[selected_period])
            
            if history.empty:
                st.warning(f"No price data found for {ticker}. It might be delisted or potentially an invalid ticker.")
                return 
        except Exception as e:
            st.error(f"Error fetching historical data for {ticker}: {e}")
            return
        # 2. Try to get info (Optional - may fail due to rate limits)
        info = {}
        try:
            info = stock.info
        except Exception:
            # If info fails, we just continue with empty info
            pass
            
        # Helper to safely get info
        def get_info(key, default=None):
            return info.get(key, default)
        # Basic Data Checks
        current_price = get_info('currentPrice')
        previous_close = get_info('previousClose')
        
        # Fallback for price if info is missing but history exists
        if current_price is None and not history.empty:
            current_price = history['Close'].iloc[-1]
            if len(history) > 1:
                previous_close = history['Close'].iloc[-2]
        
        # Calculate Deltas
        if current_price and previous_close:
            delta = current_price - previous_close
            delta_percent = (delta / previous_close) * 100
            delta_color = "green" if delta >= 0 else "red"
            delta_sign = "+" if delta >= 0 else ""
        else:
            delta = 0
            delta_percent = 0
            delta_color = "black"
            delta_sign = ""
        # Header Section
        col1, col2 = st.columns([2, 1])
        with col1:
            short_name = get_info('shortName', ticker)
            st.title(f"{short_name} ({ticker})")
            
            if current_price:
                st.markdown(f"""
                <div style="font-size: 36px; font-weight: bold;">
                    {current_price:,.2f} 
                    <span style="font-size: 20px; color: {delta_color};">
                        {delta_sign}{delta:.2f} ({delta_sign}{delta_percent:.2f}%)
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            currency = get_info('currency', 'USD')
            st.caption(f"Currency in {currency}")
        # Main Chart
        st.subheader("Price History")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history.index, 
            y=history['Close'], 
            mode='lines', 
            name='Close',
            line=dict(color='#00C805' if delta >= 0 else '#FF5000', width=2)
        ))
        fig.update_layout(
            template="plotly_white",
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        # Summary Stats
        st.subheader("Key Statistics")
        stats_cols = st.columns(4)
        
        metrics = [
            ("Market Cap", format_number(get_info('marketCap'))),
            ("P/E Ratio", format_number(get_info('trailingPE'))),
            ("Dividend Yield", f"{get_info('dividendYield') * 100:.2f}%" if get_info('dividendYield') else "N/A"),
            ("52 Wk High", get_info('fiftyTwoWeekHigh')),
            ("52 Wk Low", get_info('fiftyTwoWeekLow')),
            ("Volume", format_number(get_info('volume'))),
        ]
        
        # Display metrics in a grid
        for i, (label, value) in enumerate(metrics):
            with stats_cols[i % 4]:
                st.markdown(f"""
                <div class="metric-container" style="margin-bottom: 10px;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        # Business Summary
        st.subheader("About")
        with st.expander("Show Company Description"):
            st.write(get_info('longBusinessSummary', "No description available."))
if __name__ == "__main__":
    main()
