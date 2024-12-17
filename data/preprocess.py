from pyspark.sql import SparkSession
from pyspark.ml.feature import MinMaxScaler
from pyspark.sql.functions import col

def preprocess_data(df):
    features = df.drop(columns=['id', 'attack_cat'], errors='ignore')
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)
    return scaled_features

def calculate_remaining_features(df):
    # Calculating placeholders for features like mean, std, and variance
    if not df.empty:
        df['Bwd Packet Length Mean'] = df['Bwd Packet Length'].mean()
        df['Bwd Packet Length Std'] = df['Bwd Packet Length'].std()
        df['Flow IAT Std'] = df['Flow IAT'].std()
        df['Packet Length Variance'] = df['Packet Length'].var()
        df['Average Packet Size'] = (df['Packet Length'].mean() + df['Packet Length'].std()) / 2
        df['Idle Mean'] = df['Idle Time'].mean()
        df['Idle Max'] = df['Idle Time'].max()
        df['Idle Min'] = df['Idle Time'].min()
    return df



spark = SparkSession.builder.appName("DataPreprocessing").getOrCreate()

def preprocess_data(df):
    features = df.drop(columns=['id', 'attack_cat'], errors='ignore')
    spark_df = spark.createDataFrame(features)
    scaler = MinMaxScaler(inputCol="features", outputCol="scaledFeatures")
    scaler_model = scaler.fit(spark_df)
    scaled_data = scaler_model.transform(spark_df)
    return scaled_data