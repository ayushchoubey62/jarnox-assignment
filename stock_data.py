import yfinance as yf
import pandas as pd
import numpy as np

def fetch_and_prepare_stock_data(symbol="INFY.NS", compare_symbol="TCS.NS"):
    """
    Fetches stock data, cleans it, and calculates required and custom metrics.
    """
    print(f"Fetching data for {symbol} and {compare_symbol}...")
    
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="2y")
        
        benchmark = yf.Ticker(compare_symbol)
        df_bench = benchmark.history(period="2y")

        if df.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        
        df_bench = df_bench.reset_index()
        df_bench['Date'] = pd.to_datetime(df_bench['Date']).dt.tz_localize(None)

        df.ffill(inplace=True)
        df.bfill(inplace=True)
        
        df_bench.ffill(inplace=True)
        df_bench.bfill(inplace=True)

        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Calculate metrics for the main stock
        df['Daily_Return'] = (df['Close'] - df['Open']) / df['Open']
        df['7_Day_MA'] = df['Close'].rolling(window=7).mean()
        df['52_Week_High'] = df['High'].rolling(window=252, min_periods=1).max()
        df['52_Week_Low'] = df['Low'].rolling(window=252, min_periods=1).min()
        df['Volatility_Score'] = df['Daily_Return'].rolling(window=20).std() * np.sqrt(252)

        # --> THE FIX: Calculate Daily Return for the benchmark stock before merging <--
        df_bench['Daily_Return'] = (df_bench['Close'] - df_bench['Open']) / df_bench['Open']

        # Custom Metric B: Correlation between two companies
        merged_returns = pd.merge(
            df[['Date', 'Daily_Return']], 
            df_bench[['Date', 'Daily_Return']], 
            on='Date', 
            suffixes=('_target', '_bench')
        )
        df['Rolling_Correlation'] = merged_returns['Daily_Return_target'].rolling(window=30).corr(merged_returns['Daily_Return_bench'])

        df.dropna(inplace=True)
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].round(4)

        return df

    except Exception as e:
        print(f"Error processing data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    stock_data = fetch_and_prepare_stock_data("INFY.NS", "TCS.NS")
    
    if not stock_data.empty:
        print("\n✅ Data successfully fetched, cleaned, and transformed!")
        print("\nPreview of the latest 5 rows:")
        print(stock_data[['Date', 'Close', 'Daily_Return', '7_Day_MA', 'Volatility_Score', 'Rolling_Correlation']].tail())