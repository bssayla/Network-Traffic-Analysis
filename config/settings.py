HDFS_URL = 'http://localhost:9870'
HDFS_DIR = '/network_data'
HDFS_USER =  'root'
KAFKA_TOPIC = 'network-data'
KAFKA_SERVER = 'localhost:9092'
MODEL_PATH = '/home/bssayla/Downloads/Testing-env/info_gatering/model/bin/model_20.h5'
NETWORK_INTERFACE = 'wlp1s0'

FIELDS = [
   'id',' Flow Duration', 'Bwd Packet Length Max', ' Bwd Packet Length Min',
   ' Bwd Packet Length Mean', ' Bwd Packet Length Std', ' Flow IAT Std',
   ' Flow IAT Max', 'Fwd IAT Total', ' Fwd IAT Std', ' Fwd IAT Max',
   ' Min Packet Length', ' Max Packet Length', ' Packet Length Mean',
   ' Packet Length Std', ' Packet Length Variance', ' Average Packet Size',
   ' Avg Bwd Segment Size', 'Idle Mean', ' Idle Max', ' Idle Min'
   ]