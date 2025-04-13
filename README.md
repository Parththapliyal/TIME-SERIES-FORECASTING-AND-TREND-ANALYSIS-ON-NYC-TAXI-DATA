# 📈 Time Series Forecasting Web App

This is an interactive Streamlit web application for time series analysis and forecasting.  
It allows users to upload their own CSV datasets, visualize trends, decompose time series, and generate forecasts using ARIMA, ETS, and Prophet models.

---

## 🚀 Features

- Upload custom time series CSV files
- Select date and target columns interactively
- Plot line chart of time series
- Perform additive or multiplicative decomposition
- Forecast using:
  - ARIMA (AutoRegressive Integrated Moving Average)
  - ETS (Error, Trend, Seasonality – Exponential Smoothing)
  - Prophet (by Meta/Facebook)
- Visual output and evaluation metrics (RMSE, MAE, MSE)

---

## 📂 Files

- `app.py`: Main Streamlit app
- `requirements.txt`: Python dependencies

---

## 📦 Installation (Local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deployment

This app can be deployed for free using [Streamlit Cloud](https://streamlit.io/cloud):

1. Upload `app.py` and `requirements.txt` to a public GitHub repository
2. Go to https://streamlit.io/cloud
3. Connect your GitHub account and deploy the app

---

## 📊 Example Use Cases

- Sales and revenue forecasting
- Traffic and transport demand prediction
- Patient or hospital resource planning
- Climate and weather trend analysis

---

## 🧑‍💻 Author

Developed with ❤️ using Python and Streamlit.