from app import app
from data.storage import fetch_data_from_hdfs
from model.predict import predict
from flask import render_template
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import mpld3

FIGURE_SIZE = (5, 5)

def create_plot(fig, title):
    fig.suptitle(title)
    fig.tight_layout()
    return fig

@app.route("/")
def dashboard():
    data = fetch_data_from_hdfs()
    predictions_df = predict(data)

    # BOX PLOT
    plt.figure(figsize=FIGURE_SIZE)
    sns.boxplot(x='Predictions', y=' Packet Length Mean', data=predictions_df)
    plt.xlabel('Traffic Type (0: Normal, 1: Attack)')
    plt.ylabel('Packet Length')
    plot1 = create_plot(plt.gcf(), 'Packet Length Distribution by Traffic Type')
    box_plot_html = mpld3.fig_to_html(plot1)

    # SCATTER PLOT
    plt.figure(figsize=FIGURE_SIZE)
    colors = ['blue' if label == 0 else 'red' for label in predictions_df['Predictions']]
    plt.scatter(predictions_df[' Flow Duration'], predictions_df[' Average Packet Size'], c=colors, alpha=0.5)
    plt.xlabel('Flow Duration')
    plt.ylabel('Average Packet Size')
    plot2 = create_plot(plt.gcf(), 'Flow Duration vs Average Packet Size')
    scatter_plot_html = mpld3.fig_to_html(plot2)

    # VIOLIN PLOT
    plt.figure(figsize=FIGURE_SIZE)
    sns.violinplot(x='Predictions', y=' Flow IAT Std', data=predictions_df)
    plt.xlabel('Traffic Type (0: Normal, 1: Attack)')
    plt.ylabel('Flow IAT Standard Deviation')
    plot3 = create_plot(plt.gcf(), 'Flow IAT Distribution')
    violin_plot_html = mpld3.fig_to_html(plot3)

    # SECOND SCATTER
    plt.figure(figsize=FIGURE_SIZE)
    colors = ['blue' if label == 0 else 'red' for label in predictions_df['Predictions']]
    plt.scatter(predictions_df[' Bwd Packet Length Mean'], predictions_df[' Packet Length Mean'], c=colors, alpha=0.5)
    plt.xlabel('Backward Packet Length Mean')
    plt.ylabel('Overall Packet Length Mean')
    plot4 = create_plot(plt.gcf(), 'Packet Length Correlation')
    scatter_plot_2_html = mpld3.fig_to_html(plot4)

    # PIE PLOT (ATTACK VS NON-ATTACK)
    counts = predictions_df['Predictions'].value_counts().reindex([0,1], fill_value=0)
    labels = ['Normal', 'Attack']
    plt.figure(figsize=FIGURE_SIZE)
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plot5 = create_plot(plt.gcf(), 'Traffic Distribution')
    pie_plot_html = mpld3.fig_to_html(plot5)

    table_data = predictions_df.to_dict('records')

    # LINE CHART
    plt.figure(figsize=FIGURE_SIZE)
    green_data = predictions_df[predictions_df['Predictions'] == 0][' Flow Duration']
    red_data = predictions_df[predictions_df['Predictions'] == 1][' Flow Duration']
    plt.plot(green_data, color='green', label='Normal')
    plt.plot(red_data, color='red', label='Attack')
    plt.legend()
    plt.xlabel('Index')
    plt.ylabel('Flow Duration')
    plot6 = create_plot(plt.gcf(), 'Prediction Trends Over Time')
    line_chart_html = mpld3.fig_to_html(plot6)

    return render_template('index.html',
                           box_plot_html=box_plot_html,
                           scatter_plot_html=scatter_plot_html,
                           scatter_plot_2_html=scatter_plot_2_html,
                           violin_plot_html=violin_plot_html,
                           pie_plot_html=pie_plot_html,
                           line_chart_html=line_chart_html,
                           table_data=table_data,
                           columns=predictions_df.columns)