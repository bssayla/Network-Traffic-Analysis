from pyspark.sql import SparkSession
import pyshark
import pandas as pd
from kafka_.producer import send_to_kafka
from config.settings import NETWORK_INTERFACE

spark = SparkSession.builder.appName("NetworkCapture").getOrCreate()

def capture_network_data(output_file):
    capture = pyshark.LiveCapture(interface=NETWORK_INTERFACE)
    data = []

    for packet in capture.sniff_continuously(packet_count=50):
        try:
            packet_info = {
                'Flow Duration': packet.sniff_time.timestamp(),
                'Bwd Packet Length Max': getattr(packet, 'length', None),
                'Bwd Packet Length Min': getattr(packet, 'length', None),
                'Bwd Packet Length Mean': None,
                'Bwd Packet Length Std': None,
                'Flow IAT Std': None,
                'Flow IAT Max': None,
                'Fwd IAT Total': None,
                'Fwd IAT Std': None,
                'Fwd IAT Max': None,
                'Min Packet Length': getattr(packet, 'length', None),
                'Max Packet Length': getattr(packet, 'length', None),
                'Packet Length Mean': None,
                'Packet Length Std': None,
                'Packet Length Variance': None,
                'Average Packet Size': None,
            }
            data.append(packet_info)
        except AttributeError as e:
            print(f"Skipped packet due to error: {e}")
            continue

    # Convert to Spark DataFrame and save as JSON
    df = pd.DataFrame(data)
    spark_df = spark.createDataFrame(df)
    spark_df.write.json(output_file)

    # Send to Kafka
    send_to_kafka(output_file)
