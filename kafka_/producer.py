from kafka import KafkaProducer
from config.settings import KAFKA_TOPIC, KAFKA_SERVER

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

def send_to_kafka(file_name):
    with open(file_name, 'r') as f:
        producer.send(KAFKA_TOPIC, f.read().encode('utf-8'))
