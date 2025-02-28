from kafka import KafkaProducer
import yfinance as yf
import json
import time

# Kafka Config
KAFKA_BROKER = "localhost:9092"
TOPIC = "stock-data"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

STOCK_SYMBOL = "AAPL"  # Apple stock

while True:
    stock = yf.Ticker(STOCK_SYMBOL)
    data = stock.history(period="1d")

    if not data.empty:
        price = round(data["Close"].iloc[-1], 2)  # Get latest closing price
        message = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": STOCK_SYMBOL,
            "price": price
        }
        producer.send(TOPIC, value=message)
        print(f"Sent: {message}")

    time.sleep(1)  # Fetch stock price every minute
