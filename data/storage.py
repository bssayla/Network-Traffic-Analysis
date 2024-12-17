import os
import json
import pandas as pd
from hdfs import InsecureClient
from config.settings import HDFS_URL, HDFS_DIR, HDFS_USER

hdfs_client = InsecureClient(HDFS_URL, user=HDFS_USER)

def store_data_in_hdfs(file_name):
    file_path = os.path.join(HDFS_DIR, file_name)
    with open(file_name, 'r') as f:
        hdfs_client.write(file_path, f.read(), overwrite=True)


def fetch_data_from_hdfs():
    files = hdfs_client.list(HDFS_DIR)
    latest_file = max(files)  # Get the latest file by timestamp
    with hdfs_client.read(f"{HDFS_DIR}/{latest_file}") as reader:
        data = json.load(reader)
    df = pd.DataFrame(data)
    return df

def fetch_training_data():
    # Assuming training data is stored in a CSV file
    training_data_path = 'data/training_data/test.csv'
    df = pd.read_csv(training_data_path)
    return df
