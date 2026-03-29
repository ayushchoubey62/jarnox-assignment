# Stock Data Intelligence Dashboard 🚀

An AI-powered financial data platform built for the **Jarnox Software Internship Assignment**. This project demonstrates a full-stack approach to financial data analysis, combining real-time data fetching, RESTful API design, and machine learning.

## 🌟 Key Features
* [cite_start]**Real-time Data Collection**: Fetches live stock market data using the `yfinance` API[cite: 37].
* [cite_start]**Automated Data Cleaning**: Uses Pandas to handle missing values and format date columns properly[cite: 38, 40, 41].
* [cite_start]**Financial Metrics**: Automatically calculates **Daily Returns**, **7-day Moving Averages**, and **52-week High/Low**[cite: 43, 44, 45].
* [cite_start]**Custom Analytics**: Includes an original **Volatility Score** (annualized rolling standard deviation)[cite: 48].
* [cite_start]**AI Predictions**: Features a **Linear Regression ML model** that predicts price trends for the next 5 days based on historical patterns[cite: 61, 65].
* [cite_start]**Interactive Dashboard**: A responsive UI built with **Bootstrap** and **Chart.js** for seamless data visualization[cite: 55, 57].
* [cite_start]**API Documentation**: Includes a pre-configured **Postman Collection** for professional endpoint exploration[cite: 53].

## 🛠️ Tech Stack
* [cite_start]**Backend**: Python, Flask [cite: 27, 28]
* [cite_start]**Data Science**: Pandas, NumPy, Scikit-learn [cite: 30]
* [cite_start]**Frontend**: HTML5, JavaScript (ES6), Bootstrap 5, Chart.js [cite: 30, 31]
* [cite_start]**DevOps**: Docker, Gunicorn [cite: 66]

## 🚀 Getting Started

### [cite_start]Using Docker (Recommended) [cite: 66]
1.  **Build the image**:  
    `docker build -t stock-dashboard .`
2.  **Run the container**:  
    `docker run -p 5000:5000 stock-dashboard`
3.  **Visit**: `http://localhost:5000`

### Manual Setup
1.  **Install dependencies**:  
    `pip install -r requirements.txt` [cite: 73]
2.  **Run the application**:  
    `python app.py` [cite: 72]
3.  **Access the Dashboard**:  
    Navigate to `http://127.0.0.1:5000/` in your browser.

## [cite_start]📂 API Endpoints [cite: 52]
- `GET /companies`: Returns a list of all available companies.
- `GET /data/{symbol}`: Returns the last 30 days of stock data.
- `GET /summary/{symbol}`: Returns 52-week high, low, and average close.
- `GET /compare?symbol1=INFY.NS&symbol2=TCS.NS`: (Bonus) Compare two stocks' performance.
