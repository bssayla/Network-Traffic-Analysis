import time
from data.capture import NetworkFlowCapture
from data.storage import store_data_in_hdfs, fetch_data_from_hdfs
from model.predict import predict
from kafka import KafkaProducer
from config.settings import KAFKA_SERVER, KAFKA_TOPIC


producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

def main():
    while True:
        try:
            print("INFO: Capturing network data...")
            output_folder = 'network_data'
            capture = NetworkFlowCapture()
            try:
                capture.start_capture()
            except KeyboardInterrupt:
                print("\nCapture stopped by user")
                capture.save_to_json()
                break
            except Exception as e:
                print(f"Error during capture: {e}")

            print("INFO: Storing data in HDFS...")
            store_data_in_hdfs(output_folder)
            print("INFO: Fetching data from HDFS...")
            data = fetch_data_from_hdfs()
            print(data.head())
            print("INFO: Predicting results...")
            prediction_results = predict(data)
            print("INFO: Results:")
            print(prediction_results[['id', 'Predictions']])

            print("INFO: Sending results to Kafka...")
            predictions_json = prediction_results[['id', 'Predictions']].to_json(orient='records')
            producer.send(KAFKA_TOPIC, predictions_json.encode('utf-8'))
            producer.flush()
            print("INFO: done...")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()