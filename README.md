# **Real-Time Stock Price Prediction**

## **📌 Project Overview**
**Real-time stock price prediction system** that leverages **Kafka streaming, TensorFlow deep learning models, and Python** to analyze and predict stock prices. The system consumes live stock data, processes it through a trained neural network model, and publishes predicted prices.

## **🛠️ System Design**
### **Architecture**
The system follows a **producer-consumer model** using **Apache Kafka**:
1. **Producer:** Fetches real-time stock price data and pushes it to Kafka.
2. **Kafka Broker:** Acts as the message queue, storing stock data.
3. **Consumer:** Consumes stock data, applies a trained machine learning model, and predicts the future price.
4. **Model Training:** A deep learning model is trained using historical stock data and saved for inference.
5. **Evaluation Module:** Compares predicted prices with actual prices and calculates model performance (MSE - Mean Squared Error).

## **🚀 Installation Guide**

### 1. Kafka Installation (Local)
To run Kafka locally, follow these steps:

#### Install Kafka (Mac/Linux):
```bash
# Download Kafka
wget https://downloads.apache.org/kafka/3.4.0/kafka_2.13-3.9.0.tgz

# Extract Kafka
tar -xzf kafka_2.13-3.9.0.tgz
cd kafka_2.13-3.9.0
```

### 2. Start Kafka (Zookeeper required)
Kafka requires Zookeeper to manage brokers. Start Zookeeper first:

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &
```

Now, start the Kafka broker:
```bash
# Start Kafka server
bin/kafka-server-start.sh config/server.properties &
```

### 3. Create Kafka Topics

Create Kafka topics for communication between producer and consumer.
```bash
# Create the input topic (Stock Price Data)
bin/kafka-topics.sh --create --topic stock_prices --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Create the output topic (Predicted Prices)
bin/kafka-topics.sh --create --topic predicted_prices --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. Summary of Kafka Topics
- **`stock_prices`**: Receives real-time stock price updates from the producer.
- **`predicted_prices`**: Stores the output from the consumer after predicting stock prices.

## **🖥️ Implementation Details**

### **🔹 1. Data Producer (producer.py)**
  The model was trained using historical stock price data obtained from publicly available Yahoo Finance  financial datasets. The dataset included:
- Stock Symbols: AAPL, MSFT, AMZN, etc.
- Date Range: 2015-2024 (10 years of data)
- Fetches stock data (e.g., `AAPL` stock price) from an external source.
- Publishes JSON messages to a Kafka topic (`stock_prices`).
- Message format:
  ```json
  {
    "timestamp": "2025-02-27 21:54:55",
    "symbol": "AAPL",
    "price": 242.08
  }
  ```

### **🔹 2. Model Training (train_model.py)**
- Loads historical stock price data.
- Prepares training and testing datasets.
- Builds a **TensorFlow deep learning model** (e.g., LSTM/GRU for time-series forecasting).
- Saves the trained model as `stock_model.h5`.

### **🔹 3. Data Consumer & Prediction (consumer.py)**
- Reads incoming stock price data from Kafka.
- Loads the pre-trained **stock_model.h5**.
- Runs predictions using TensorFlow.
- Publishes the **predicted price** to another Kafka topic (`predicted_prices`).
- Handles real-time data serialization and deserialization.

### **🔹 4. Model Evaluation (evaluate.py)**
- Compares predicted prices with actual prices.
- Computes **Mean Squared Error (MSE)** as the evaluation metric.
- Outputs performance results.

## **📊 Evaluation Results**
After running the **evaluate.py** script, the model achieved:
- **Mean Squared Error (MSE):** `3.6187`

This indicates the **average squared difference** between predicted and actual prices. Lower MSE values represent better accuracy.

## **🚀 Run the Project**
### **1️⃣ Start Kafka Server**
Ensure Kafka is running locally or in a cloud environment:
```sh
kafka-server-start.sh config/server.properties
```

### **2️⃣ Train the Model **
To retrain the model using historical stock data:
```sh
python train_model.py
```
## Console Output

```bash
(base) ranjoysen@ranjoy KafkaNeuroPredict % python train_model.py
Epoch 1/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - loss: 0.2623 - mae: 0.4463 
Epoch 2/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0234 - mae: 0.1253 
Epoch 3/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0071 - mae: 0.0681 
Epoch 4/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0056 - mae: 0.0611 
Epoch 5/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0051 - mae: 0.0597 
Epoch 6/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0047 - mae: 0.0577 
Epoch 7/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0046 - mae: 0.0552 
Epoch 8/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - loss: 0.0039 - mae: 0.0515 
Epoch 9/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0046 - mae: 0.0564 
Epoch 10/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0041 - mae: 0.0532 
Epoch 11/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0037 - mae: 0.0507 
Epoch 12/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0050 - mae: 0.0570 
Epoch 13/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0041 - mae: 0.0528 
Epoch 14/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0035 - mae: 0.0485 
Epoch 15/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0036 - mae: 0.0478 
Epoch 16/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0041 - mae: 0.0504 
Epoch 17/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - loss: 0.0029 - mae: 0.0440 
Epoch 18/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0030 - mae: 0.0441 
Epoch 19/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0030 - mae: 0.0436 
Epoch 20/20
31/31 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - loss: 0.0028 - mae: 0.0414 
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`. 
Model Training Complete. Saved as stock_model.h5
```

### **3️⃣ Start the Data Producer**
Run the producer to fetch stock data and send it to Kafka:
```sh
python producer.py
```
## Console Output

```bash
(base) ranjoysen@ranjoy KafkaNeuroPredict % python producer.py
Sent: {'timestamp': '2025-02-27 22:18:25', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:26', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:27', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:29', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:30', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:31', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:32', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:33', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:34', 'symbol': 'AAPL', 'price': 240.93}
Sent: {'timestamp': '2025-02-27 22:18:36', 'symbol': 'AAPL', 'price': 240.92}
Sent: {'timestamp': '2025-02-27 22:18:37', 'symbol': 'AAPL', 'price': 240.92}
Sent: {'timestamp': '2025-02-27 22:18:38', 'symbol': 'AAPL', 'price': 240.92}
Sent: {'timestamp': '2025-02-27 22:18:39', 'symbol': 'AAPL', 'price': 240.92}
```

### **4️⃣ Start the Consumer for Predictions**
```sh
python consumer.py
```
## Console Output

```bash
(base) ranjoysen@ranjoy KafkaNeuroPredict % python consumer.py
Received: {'timestamp': '2025-02-27 22:15:51', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:52', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:54', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:55', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:56', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:57', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:58', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:15:59', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:16:00', 'symbol': 'AAPL', 'price': 241.05}
Received: {'timestamp': '2025-02-27 22:16:01', 'symbol': 'AAPL', 'price': 241.05}
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 348ms/step
Predicted: {'timestamp': '2025-02-27 22:16:02', 'actual_price': 241.05, 'predicted_price': 239.2}
Received: {'timestamp': '2025-02-27 22:16:03', 'symbol': 'AAPL', 'price': 241.07}
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 48ms/step
Predicted: {'timestamp': '2025-02-27 22:16:03', 'actual_price': 241.07, 'predicted_price': 239.21}
Received: {'timestamp': '2025-02-27 22:16:04', 'symbol': 'AAPL', 'price': 241.07}
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 44ms/step
Predicted: {'timestamp': '2025-02-27 22:16:04', 'actual_price': 241.07, 'predicted_price': 239.21}
Received: {'timestamp': '2025-02-27 22:16:05', 'symbol': 'AAPL', 'price': 241.07}
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 51ms/step
Predicted: {'timestamp': '2025-02-27 22:16:05', 'actual_price': 241.07, 'predicted_price': 239.22}
Received: {'timestamp': '2025-02-27 22:16:06', 'symbol': 'AAPL', 'price': 241.07}
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 47ms/step
Predicted: {'timestamp': '2025-02-27 22:16:06', 'actual_price': 241.07, 'predicted_price': 239.22}
Received: {'timestamp': '2025-02-27 22:16:07', 'symbol': 'AAPL', 'price': 241.07}
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 50ms/step
Predicted: {'timestamp': '2025-02-27 22:16:07', 'actual_price': 241.07, 'predicted_price': 239.22}
Received: {'timestamp': '2025-02-27 22:16:08', 'symbol': 'AAPL', 'price': 241.07}
```

### **5️⃣ Evaluate Model Performance**
```sh
python evaluate.py
```
## Console Output

```bash
(base) ranjoysen@ranjoy KafkaNeuroPredict % python evaluate.py

Mean Squared Error: 3.6187179999999723
Mean Squared Error: 3.6766220000000267
Mean Squared Error: 3.6950100000000208
Mean Squared Error: 3.656568000000023
Mean Squared Error: 3.6115679999999704
Mean Squared Error: 3.541546000000009
Mean Squared Error: 3.5346280000000103
Mean Squared Error: 3.5701959999999895
Mean Squared Error: 3.468105999999989
Mean Squared Error: 3.482055999999984
Mean Squared Error: 3.503291999999969
Mean Squared Error: 3.537780000000002
Mean Squared Error: 3.5318200000000157
Mean Squared Error: 3.456369999999959
Mean Squared Error: 3.4262379999999992
Mean Squared Error: 3.3784040000000086
```

## **📌 Key Features**
✅ **Real-time stock price streaming** with Apache Kafka.  
✅ **Deep learning model** (LSTM/GRU) for time-series forecasting.  
✅ **Scalable and modular architecture** for future enhancements.  
✅ **Performance evaluation** with Mean Squared Error.  

