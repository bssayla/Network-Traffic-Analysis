# from pyspark.sql import SparkSession
# from pyspark.sql.types import StructType, StructField, DoubleType
import pyshark
# import pandas as pd
from kafka_.producer import send_to_kafka
from config.settings import NETWORK_INTERFACE
import pyshark
import json
from time import time
from datetime import datetime
import os
import numpy as np

class NetworkFlowCapture:
    def __init__(self):
        self.flow_metrics = {
            "Flow Duration": [],
            "Bwd Packet Length": [],
            "Flow IAT": [],
            "Fwd IAT": [],
            "Packet Length": [],
            "Packet Size": [],
            "Idle": [],
            "Bwd Segment Size": []
        }
        self.flow_start_time = None
        self.last_packet_time = None
        self.forward_direction = None
        self.last_activity_time = None
        
    def process_packet(self, packet):
        try:
            current_time = time()
            
            # Initialize flow start time if this is the first packet
            if self.flow_start_time is None:
                self.flow_start_time = current_time
                self.last_activity_time = current_time
                if hasattr(packet, 'ip'):
                    self.forward_direction = (packet.ip.src, packet.tcp.srcport if hasattr(packet, 'tcp') else None)
            
            # Calculate flow duration
            flow_duration = current_time - self.flow_start_time
            self.flow_metrics["Flow Duration"].append(flow_duration)
            
            # Calculate packet length and size
            packet_length = int(packet.length)
            self.flow_metrics["Packet Length"].append(packet_length)
            self.flow_metrics["Packet Size"].append(packet_length) 
            
            # Calculate idle time (time since last activity)
            idle_time = current_time - self.last_activity_time
            self.flow_metrics["Idle"].append(idle_time)
            self.last_activity_time = current_time
            
            # Process TCP-specific metrics if available
            if hasattr(packet, 'tcp'):
                # Determine packet direction and calculate backward metrics
                current_direction = (packet.ip.src, packet.tcp.srcport)
                if self.forward_direction and current_direction != self.forward_direction:
                    self.flow_metrics["Bwd Packet Length"].append(packet_length)
                    
                    # Calculate Backward Segment Size
                    # TCP segment size is the payload size (total length - IP header - TCP header)
                    if hasattr(packet, 'ip'):
                        ip_header_length = int(packet.ip.hdr_len)
                        tcp_header_length = int(packet.tcp.hdr_len)
                        segment_size = packet_length - ip_header_length - tcp_header_length
                        self.flow_metrics["Bwd Segment Size"].append(segment_size)
            
            # Calculate Inter-Arrival Time (IAT)
            if self.last_packet_time is not None:
                iat = current_time - self.last_packet_time
                self.flow_metrics["Flow IAT"].append(iat)
                
                # Calculate forward IAT based on direction
                if hasattr(packet, 'ip'):
                    current_direction = (packet.ip.src, packet.tcp.srcport if hasattr(packet, 'tcp') else None)
                    if current_direction == self.forward_direction:
                        self.flow_metrics["Fwd IAT"].append(iat)
            
            self.last_packet_time = current_time
            
        except Exception as e:
            print(f"Error processing packet: {e}")


    def start_capture(self, interface=NETWORK_INTERFACE, packet_count=50):
        """
        Start capturing packets on the specified interface
        
        Args:
            interface (str): Network interface to capture from
            packet_count (int): Number of packets to capture
        """
        print(f"Starting capture on interface {interface}...")
        
        # Create a capture object
        capture = pyshark.LiveCapture(interface=interface)
        
        # Process packets
        for packet in capture.sniff_continuously(packet_count=packet_count):
            self.process_packet(packet)
            
        # Save metrics to JSON file after capture
        self.save_to_json()
    
    def save_to_json(self, folder_name="network_data"):
        """
        Save captured metrics to a JSON file
        """
        # Create the directory if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flow_metrics_{timestamp}.json"
        
        # Calculate some basic statistics for each metric
        flow_stats = {
            metric: {
                "values": values,
                "statistics": {
                    "count": int(len(values)),
                    "min": float(np.min(values)) if values else None,
                    "sum": float(np.sum(values)) if values else None,
                    "max": float(np.max(values)) if values else None,
                    "average": float(np.mean(values)) if values else None,
                    "std": float(np.std(values)) if values else None,
                }
            }
            for metric, values in self.flow_metrics.items()
        }
        
        # Save to JSON file
        try:
            with open(f"{folder_name}/{filename}", "w") as f:
                json.dump(flow_stats, f, indent=4)
            print(f"Flow metrics saved to {folder_name}/{filename}")
            send_to_kafka(f"{folder_name}/{filename}")
        except Exception as e:
            print(f"Error saving flow metrics: {e}")


