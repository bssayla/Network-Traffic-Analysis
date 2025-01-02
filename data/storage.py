import os
import json
import pandas as pd
from hdfs import InsecureClient
from config.settings import HDFS_URL, HDFS_DIR, HDFS_USER, FIELDS
from data.preprocess import calculate_remaining_features

hdfs_client = InsecureClient(HDFS_URL, user=HDFS_USER)

def store_data_in_hdfs(folder_name:str) -> None:
    # get only json files and store them in HDFS as json
    files = [f for f in os.listdir(folder_name) if f.endswith('.json')]
    for file in files:
        hdfs_client.upload(HDFS_DIR, f"{folder_name}/{file}", overwrite=True)
        


def fetch_data_from_hdfs()->pd.DataFrame:
    # each file going to be a row in the dataframe
    data = pd.DataFrame(columns=FIELDS)
    # get all files from HDFS
    files = hdfs_client.list(HDFS_DIR)
    rows = []
    for i, file in enumerate(files):
        with hdfs_client.read(f"{HDFS_DIR}/{file}") as reader:
            json_data = json.load(reader)
            # create a row from the json data
            row = calculate_remaining_features(i, json_data)
            rows.append(row)
    
    data = pd.concat([data, pd.DataFrame(rows)], ignore_index=True)
    print("INFO: data fetched")
    return data