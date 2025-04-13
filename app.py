#!/usr/bin/env python
# coding: utf-8

# In[1]:


# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error

st.set_page_config(page_title="Time Series Forecasting App", layout="wide")
st.title("📈 Time Series Forecasting Web App")

# Upload CSV
uploaded_file = st.file_uploader("Upload your time series CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Step 1: Choose Columns")
    date_col = st.selectbox("Select Date Column", df.columns)
    target_col = st.selectbox("Select Target Column", df.columns)

    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)
    df = df[[target_col]].dropna()

    st.line_chart(df, use_container_width=True)

    # Decomposition
    st.subheader("Step 2: Time Series Decomposition")
    model_type = st.radio("Decomposition Type", ["Additive", "Multiplicative"])
    period = st.number_input("Seasonal Period (e.g., 12 for monthly)", value=12, min_value=2)

    if st.button("Decompose"):
        result = seasonal_decompose(df[target_col], model=model_type.lower(), period=period)
        fig, axs = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
        result.observed.plot(ax=axs[0], title="Observed")
        result.trend.plot(ax=axs[1], title="Trend")
        result.seasonal.plot(ax=axs[2], title="Seasonality")
        result.resid.plot(ax=axs[3], title="Residuals")
        st.pyplot(fig)

    # Forecasting
    st.subheader("Step 3: Forecasting")
    model_choice = st.selectbox("Choose Forecasting Model", ["ARIMA", "ETS", "Prophet"])
    forecast_period = st.slider("Forecast Horizon (in steps)", 7, 60, 30)

    train = df[target_col][:-forecast_period]
    test = df[target_col][-forecast_period:]

    forecast = None

    if st.button("Run Forecast"):
        if model_choice == "ARIMA":
            model = ARIMA(train, order=(1, 1, 1)).fit()
            forecast = model.forecast(steps=forecast_period)
        
        elif model_choice == "ETS":
            model = ExponentialSmoothing(train, seasonal='add', seasonal_periods=period).fit()
            forecast = model.forecast(forecast_period)

        elif model_choice == "Prophet":
            prophet_df = df.reset_index().rename(columns={date_col: "ds", target_col: "y"})
            model = Prophet()
            model.fit(prophet_df)
            future = model.make_future_dataframe(periods=forecast_period)
            forecast_df = model.predict(future)
            forecast = forecast_df.set_index("ds")["yhat"].loc[test.index]

        # Plot forecast
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(train.index, train, label="Train")
        ax.plot(test.index, test, label="Test", color='green')
        ax.plot(test.index, forecast, label="Forecast", linestyle="--", color='red')
        ax.legend()
        st.pyplot(fig)

        # Metrics
        st.subheader("Evaluation Metrics")
        rmse = np.sqrt(mean_squared_error(test, forecast))
        mae = mean_absolute_error(test, forecast)
        mape = np.mean(np.abs((test - forecast) / test)) * 100
        mse = mean_squared_error(test, forecast)

        st.write(f"**RMSE**: {rmse:.2f}")
        st.write(f"**MAE**: {mae:.2f}")
        st.write(f"**MAPE**: {mape:.2f}%")
        st.write(f"**MSE**: {mse:.2f}")


# In[ ]:




