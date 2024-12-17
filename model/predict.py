import tensorflow as tf
from config.settings import MODEL_PATH
from data.preprocess import preprocess_data

model = tf.keras.models.load_model(MODEL_PATH)

def predict(data):
    return model.predict(data)

def predict_with_model(df):
    # Preprocess data
    preprocessed_data, _ = preprocess_data(df)
    
    # Predict using the model
    predictions = model.predict(preprocessed_data)
    
    # Attach predictions to the dataframe
    df['Predictions'] = np.argmax(predictions, axis=1)  # Assuming multi-class classification
    return df