import json
import pandas as pd
from kafka import KafkaConsumer
from config.settings import KAFKA_TOPIC, KAFKA_SERVER
from data.preprocess import preprocess_data
from model.predict import predict

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER, auto_offset_reset='latest')

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER, auto_offset_reset='latest')

def consume_data():
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        df = pd.DataFrame([data])
        preprocessed_data = preprocess_data(df)
        predictions = predict(preprocessed_data)
        print(predictions)

if __name__ == '__main__':
    consume_data()