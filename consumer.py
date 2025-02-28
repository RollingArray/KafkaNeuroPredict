from kafka import KafkaConsumer, KafkaProducer
import tensorflow as tf
import joblib
import json
import numpy as np
import time

# Kafka Config
KAFKA_BROKER = "localhost:9092"
INPUT_TOPIC = "stock-data"
OUTPUT_TOPIC = "predictions"

# Load Trained Model and Scaler
model = tf.keras.models.load_model("stock_model.h5")
scaler = joblib.load("scaler.pkl")

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest"
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

LOOKBACK = 10
prices = []

for message in consumer:
    data = message.value
    price = float(data["price"])  # Ensure it's a float
    
    print(f"Received: {data}")

    # Store last 10 prices
    prices.append(price)
    if len(prices) > LOOKBACK:
        prices.pop(0)

    # Ensure we have enough data for prediction
    if len(prices) == LOOKBACK:
        input_data = np.array(prices).reshape(-1, 1)  # Reshape to (10, 1)
        input_scaled = scaler.transform(input_data)  # Scale the data
        
        # Reshape for LSTM (batch_size=1, time_steps=10, features=1)
        input_scaled = input_scaled.reshape(1, LOOKBACK, 1)

        # Make Prediction
        prediction = model.predict(input_scaled)
        predicted_price = scaler.inverse_transform(prediction)[0][0]  # Convert back

        # Create Kafka message
        result = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_price": price,
            "predicted_price": round(float(predicted_price), 2)
        }

        producer.send(OUTPUT_TOPIC, value=result)
        print(f"Predicted: {result}")
