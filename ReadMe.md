# Network Attack Detection

## Overview

This project aims to detect network attacks using machine learning models. It captures network flow data, preprocesses it, trains a classification model, and visualizes the results on a dashboard.

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── routes.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── spark.py
├── data/
│   ├── __init__.py
│   ├── capture.py
│   ├── preprocess.py
│   ├── storage.py
│   ├── training_data/
├── kafka_/
│   ├── __init__.py
│   ├── consumer.py
│   ├── producer.py
├── model/
│   ├── __init__.py
│   ├── bin/
│   ├── model.py
│   ├── predict.py
├── network_data/
│   ├── flow_metrics_*.json
├── notebooks/
│   ├── attack-detection-on-networks.ipynb
├── static/
├── templates/
│   ├── index.html
├── .gitignore
├── app.py
├── main.py
├── ReadMe.md
├── requirements.txt
```

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-repo/network-attack-detection.git
    cd network-attack-detection
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Update the configuration settings in 

settings.py

 as needed:
- HDFS_URL
- HDFS_DIR
- HDFS_USER
- KAFKA_TOPIC
- KAFKA_SERVER
- MODEL_PATH
- NETWORK_INTERFACE: you can check using the command `ifconfig` in the terminal
- FIELDS

## Usage

### Running the Application

1. **Start the zookeeper server:**
    ```sh
    zookeeper-server-start.sh config/zookeeper.properties
    ```
2. **Start the Kafka on your machine:**
    ```sh
    kafka-server-start.sh config/server.properties
    ```
3. **Start hdfs:**
    ```sh
    start-all.sh
    ```
4. **Start the Flask application:**
    ```sh
    python app.py
    ```

5. **Run the main script to capture data and make predictions:**
    ```sh
    python main.py
    ```


### Jupyter Notebooks

The attack-detection-on-networks.ipynb

notebook contains the data preprocessing, model training, and evaluation steps. Open the notebook using Jupyter and run the cells to see the results or change the code as needed.

### Kafka

The project uses Kafka for streaming data. Ensure Kafka is running and configured correctly. The Kafka producer sends flow metrics to the specified topic.

## Dashboard

The dashboard visualizes the results using various plots:
- **Pie Chart:** Distribution of normal and attack traffic.
- **Line Chart:** Prediction trends over time.
- **Box Plot:** Distribution of packet lengths by traffic type.
- **Scatter Plot:** Relationship between flow duration and average packet size.
- **Violin Plot:** Flow IAT standard deviation distribution by traffic type.

Access the dashboard at `http://localhost:5000`.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**
    ```sh
    git checkout -b feature-branch
    ```
3. **Make your changes and commit them:**
    ```sh
    git commit -m 'Add some feature'
    ```
4. **Push to the branch:**
    ```sh
    git push origin feature-branch
    ```
5. **Submit a pull request.**


## Acknowledgements

- Mohamed Ouaicha
- Moussa Aoukacha
- Yassine Amarir