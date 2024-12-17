from flask import render_template, jsonify
from app import app
from kafka_.consumer import consume_data
from data.storage import fetch_training_data
import pandas as pd
@app.route("/")
def dashboard():
    predictions = consume_data()
    return render_template("templates/dashboard.html", predictions=predictions)

@app.route("/training-data")
def training_data():
    df = fetch_training_data()
    table_html = df.to_html(classes="table table-striped", index=False)
    return render_template("templates/index.html", table_html=table_html)
