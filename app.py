from flask import render_template, jsonify
from flask import Flask
from app import app
from kafka_.consumer import consume_data
from data.storage import fetch_data_from_hdfs
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Fetch the data
    df = fetch_data_from_hdfs()
    
    # Generate the visualization
    y = df[' Label']
    plt.figure(figsize=(10, 6))
    plt.plot(y, color='blue', marker='o')

    
    # Save the visualization as an image
    img_path = "static/images/flow_duration_distribution.png"
    plt.savefig(img_path)
    plt.close()
    
    # Render the template with the image
    return render_template('dashboard.html', image_path=img_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)