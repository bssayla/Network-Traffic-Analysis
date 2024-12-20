import tensorflow as tf
from config.settings import MODEL_PATH
from data.preprocess import preprocess_data
import numpy as np

model = tf.keras.models.load_model(MODEL_PATH)

def predict(df):
    features = preprocess_data(df.drop(columns=['id']))
    predictions = model.predict(features)
    df['Predictions'] = np.argmax(predictions, axis=1)
    return df