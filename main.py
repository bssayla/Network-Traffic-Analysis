import time
from data.capture import capture_network_data
from data.storage import store_data_in_hdfs, fetch_data_from_hdfs
from data.preprocess import calculate_remaining_features
from model.predict import predict

def main():
    while True:
        try:
            output_file = 'network_data.json'
            capture_network_data(output_file)
            store_data_in_hdfs(output_file)
            raw_data = fetch_data_from_hdfs()
            processed_data = calculate_remaining_features(raw_data)
            prediction_results = predict(processed_data)
            print(prediction_results[['id', 'Predictions']])

            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()