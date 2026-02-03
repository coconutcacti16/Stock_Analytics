# Stock Analytics App

A professional stock analysis web application built with Streamlit, yfinance, and Plotly. This app mimics the "Yahoo Finance" experience, allowing users to search for stocks and view real-time data, historical charts, and key financial metrics.

## Features
- **Real-Time Data**: Fetches the latest stock price and daily change.
- **Interactive Charts**: dynamic line charts for various time periods (1M, 3M, 6M, YTD, 1Y, 5Y, MAX).
- **Key Metrics**: Displays Market Cap, P/E Ratio, Dividend Yield, and 52-Week High/Low.
- **Company Profile**: Shows the business summary for the selected stock.

## Local Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/coconutcacti16/Stock_Analytics.git
   cd Stock_Analytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Deployment

### Streamlit Community Cloud (Recommended)
This is the easiest way to deploy your app for free.

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit of Stock Analytics App"
   git push origin main
   ```
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign up/login.
3. Click "New App".
4. Select your repository (`coconutcacti16/Stock_Analytics`), branch (`main` or `master`), and main file path (`app.py`).
5. Click **Deploy!**

### Other Clouds
You can also deploy to platforms like Heroku, Render, or Railway by connecting your GitHub repository and setting the build command to `pip install -r requirements.txt` and the start command to `streamlit run app.py`.
