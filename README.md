# Stock Data Intelligence Dashboard 🚀

An AI-powered financial data platform built for the **Jarnox Software Internship Assignment**. This project demonstrates a full-stack approach to financial data analysis, combining real-time data fetching, RESTful API design, and machine learning.

## 🌟 Key Features
* **Real-time Data Collection**: Fetches live stock market data using the `yfinance` API.
* **Automated Data Cleaning**: Uses Pandas to handle missing values and format date columns properly.
* **Financial Metrics**: Automatically calculates **Daily Returns**, **7-day Moving Averages**, and **52-week High/Low**.
* **Custom Analytics**: Includes an original **Volatility Score** (annualized rolling standard deviation).
* **AI Predictions**: Features a **Linear Regression ML model** that predicts price trends for the next 5 days based on historical patterns.
* **Interactive Dashboard**: A responsive UI built with **Bootstrap** and **Chart.js** for seamless data visualization.
* **API Documentation**: Includes a pre-configured **Postman Collection** for professional endpoint exploration.

## 🛠️ Tech Stack
* **Backend**: Python, Flask
* **Data Science**: Pandas, NumPy, Scikit-learn
* **Frontend**: HTML5, JavaScript (ES6), Bootstrap 5, Chart.js
* **DevOps**: Docker, Gunicorn

## 🚀 Getting Started

### Using Docker (Recommended)
1.  **Build the image**:  
    `docker build -t stock-dashboard .`
2.  **Run the container**:  
    `docker run -p 5000:5000 stock-dashboard`
3.  **Visit**: `http://localhost:5000`

### Manual Setup
1.  **Install dependencies**:  
    `pip install -r requirements.txt`
2.  **Run the application**:  
    `python app.py`
3.  **Access the Dashboard**:  
    Navigate to `http://127.0.0.1:5000/` in your browser.

## 📂 API Endpoints
- `GET /companies`: Returns a list of all available companies.
- `GET /data/{symbol}`: Returns the last 30 days of stock data.
- `GET /summary/{symbol}`: Returns 52-week high, low, and average close.
- `GET /compare?symbol1=INFY.NS&symbol2=TCS.NS`: (Bonus) Compare two stocks' performance.
