from kafka import KafkaConsumer
import json
import numpy as np

KAFKA_BROKER = 'localhost:9092'
PREDICTION_TOPIC = 'predictions'

consumer = KafkaConsumer(
    PREDICTION_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

actual_prices = []
predicted_prices = []

for msg in consumer:
    data = msg.value
    actual_prices.append(data["actual_price"])
    predicted_prices.append(data["predicted_price"])
    
    if len(actual_prices) >= 50:  # Compute MSE every 50 messages
        mse = np.mean((np.array(actual_prices) - np.array(predicted_prices))**2)
        print(f"Mean Squared Error: {mse}")
        actual_prices, predicted_prices = [], []  # Reset
