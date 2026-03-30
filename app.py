from flask import Flask, jsonify, request, render_template
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

app = Flask(__name__)

AVAILABLE_COMPANIES = {
    "INFY.NS": "Infosys Limited",
    "TCS.NS": "Tata Consultancy Services",
    "RELIANCE.NS": "Reliance Industries",
    "HDFCBANK.NS": "HDFC Bank",
    "TATAMOTORS.NS": "Tata Motors",
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc. (Google)",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corporation"
}

def fetch_single_stock_data(symbol: str) -> pd.DataFrame:
    """Helper function to fetch and process data for API endpoints."""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="1y") 
        
        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        
        df.ffill(inplace=True)
        df.bfill(inplace=True)
        
        df['Daily_Return'] = (df['Close'] - df['Open']) / df['Open']
        df['7_Day_MA'] = df['Close'].rolling(window=7).mean()
        df['52_Week_High'] = df['High'].rolling(window=252, min_periods=1).max()
        df['52_Week_Low'] = df['Low'].rolling(window=252, min_periods=1).min()
        
        df.dropna(inplace=True)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].round(4)
        
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return pd.DataFrame()

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def home():
    """Serves the main dashboard HTML page."""
    return render_template('index.html')

@app.route('/companies', methods=['GET'])
def get_companies():
    """Returns a list of all available companies."""
    companies_list = [{"symbol": k, "name": v} for k, v in AVAILABLE_COMPANIES.items()]
    return jsonify(companies_list)

@app.route('/data/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Returns historical data AND an ML prediction for the future."""
    # Get the 'days' filter from the URL (default to 30 if not provided)
    days_to_fetch = int(request.args.get('days', 30))
    
    df = fetch_single_stock_data(symbol)
    if df.empty:
        return jsonify({"error": "Stock data not found."}), 404
    
    # 1. Prepare Historical Data
    historical_df = df.tail(days_to_fetch).copy()
    
    # 2. --- ML PREDICTION LOGIC ---
    # We use the historical closing prices to train a Linear Regression model
    df_train = historical_df[['Date', 'Close']].copy()
    df_train['Day_Index'] = np.arange(len(df_train))
    
    X = df_train[['Day_Index']] # Features (Time)
    y = df_train['Close']       # Target (Price)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict the next 5 days
    future_days = 5
    last_index = df_train['Day_Index'].iloc[-1]
    future_indices = np.arange(last_index + 1, last_index + 1 + future_days).reshape(-1, 1)
    predictions = model.predict(future_indices)
    
    # Generate future dates for the prediction
    last_date = pd.to_datetime(df_train['Date'].iloc[-1])
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, future_days + 1)]
    
    # 3. Format Output
    historical_df['Date'] = historical_df['Date'].astype(str)
    
    prediction_data = [
        {"Date": str(date.date()), "Predicted_Close": round(pred, 2)}
        for date, pred in zip(future_dates, predictions)
    ]
    
    return jsonify({
        "historical": historical_df.to_dict(orient="records"),
        "predictions": prediction_data
    })

@app.route('/summary/<symbol>', methods=['GET'])
def get_stock_summary(symbol):
    """Returns 52-week high, low, and average close."""
    df = fetch_single_stock_data(symbol)
    if df.empty:
        return jsonify({"error": "Stock data not found."}), 404
    
    latest_data = df.iloc[-1]
    avg_close = round(df['Close'].mean(), 2)
    
    return jsonify({
        "symbol": symbol,
        "52_week_high": latest_data['52_Week_High'],
        "52_week_low": latest_data['52_Week_Low'],
        "average_close": avg_close
    })

@app.route('/compare', methods=['GET'])
def compare_stocks():
    """Compare two stocks' performance."""
    symbol1 = request.args.get('symbol1')
    symbol2 = request.args.get('symbol2')

    if not symbol1 or not symbol2:
        return jsonify({"error": "Please provide both symbol1 and symbol2 as query parameters."}), 400

    df1 = fetch_single_stock_data(symbol1)
    df2 = fetch_single_stock_data(symbol2)
    
    if df1.empty or df2.empty:
        return jsonify({"error": "One or both stock symbols not found."}), 404
    
    return_1 = ((df1.iloc[-1]['Close'] - df1.iloc[0]['Close']) / df1.iloc[0]['Close']) * 100
    return_2 = ((df2.iloc[-1]['Close'] - df2.iloc[0]['Close']) / df2.iloc[0]['Close']) * 100
    
    return jsonify({
        "comparison": f"{symbol1} vs {symbol2}",
        symbol1: {
            "current_price": df1.iloc[-1]['Close'],
            "1_year_return_percent": round(return_1, 2)
        },
        symbol2: {
            "current_price": df2.iloc[-1]['Close'],
            "1_year_return_percent": round(return_2, 2)
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)