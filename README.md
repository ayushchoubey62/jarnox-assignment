# Stock Data Intelligence Dashboard 🚀

An AI-powered financial data platform built for the Jarnox Software Internship Assignment.

## 🌟 Key Features
- [cite_start]**Real-time Data**: Fetches live stock data using the `yfinance` API[cite: 37].
- [cite_start]**Custom Analytics**: Includes Volatility Scores and 7-day Moving Averages[cite: 44, 48].
- [cite_start]**AI Predictions**: Uses a **Linear Regression ML model** to predict price trends for the next 5 days[cite: 61, 65].
- [cite_start]**Interactive UI**: Built with Bootstrap and Chart.js for seamless data visualization[cite: 57].
- [cite_start]**API Documentation**: Includes a pre-configured **Postman Collection** for easy testing.

## 🛠️ Tech Stack
- [cite_start]**Backend**: Python, Flask [cite: 27, 28]
- [cite_start]**Data**: Pandas, NumPy, Scikit-learn [cite: 30]
- [cite_start]**Frontend**: HTML, JavaScript, Bootstrap, Chart.js [cite: 30, 31]
- [cite_start]**DevOps**: Docker 

## 🚀 Getting Started
### Using Docker (Recommended)
1. Build the image: `docker build -t stock-dashboard .`
2. Run the container: `docker run -p 5000:5000 stock-dashboard`
3. Visit `http://localhost:5000`

### Manual Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
