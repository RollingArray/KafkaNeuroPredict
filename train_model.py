import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib

STOCK_SYMBOL = "AAPL"
LOOKBACK = 10  # Use past 10 days' prices to predict the next day

# Fetch historical stock data from Yahoo Finance - Stock Market Live, Quotes, Business
stock = yf.Ticker(STOCK_SYMBOL)
data = stock.history(period="1y")  # Fetch 1 year of data
prices = data["Close"].values.reshape(-1, 1)

# Normalize data
scaler = MinMaxScaler()
prices_scaled = scaler.fit_transform(prices)

# Prepare training data
X, y = [], []
for i in range(len(prices_scaled) - LOOKBACK):
    X.append(prices_scaled[i : i + LOOKBACK])
    y.append(prices_scaled[i + LOOKBACK])

X, y = np.array(X), np.array(y)

# Build LSTM Model
model = Sequential([
    LSTM(50, activation="relu", return_sequences=True, input_shape=(LOOKBACK, 1)),
    LSTM(50, activation="relu"),
    Dense(1)
])

model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
model.fit(X, y, epochs=20, batch_size=8)

# Save Model and Scaler
model.save("stock_model.h5")
joblib.dump(scaler, "scaler.pkl")

print("Model Training Complete. Saved as stock_model.h5")
