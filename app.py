from flask import Flask, request, render_template, redirect, url_for
import time
from config import DATASET_ID, TABLE_ID, RAW_FILE_PATH, TOPIC_PATH
from data_processing import load_and_preprocess_data
from bigquery_operations import load_data_to_bigquery, query_prediction
from pubsub_operations import publish_message
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            logging.debug(f'File uploaded received')
            file.save(RAW_FILE_PATH)
            return redirect(url_for('process_data'))
        else:
            logging.error(f'No file uploaded')
    return render_template('index.html')

@app.route('/process_data', methods=['GET'])
def process_data():
    try:
        # Load and preprocess the raw data
        df = load_and_preprocess_data(RAW_FILE_PATH, 'csv')

        # Measure data load time
        start_time = time.time()
        load_job = load_data_to_bigquery(df, DATASET_ID, TABLE_ID)
        end_time = time.time()
        load_duration = end_time - start_time

        # Log `TOPIC_PATH` and success message
        success_message = {'event': 'data_loaded', 'status': 'success', 'table': f'{DATASET_ID}.{TABLE_ID}', 'duration': load_duration}
        logging.debug(f'TOPIC_PATH: {TOPIC_PATH}')
        logging.debug(f'Success message: {success_message}')

        # Error handling
        if load_job.error_result is None:
            publish_message(TOPIC_PATH, success_message)
            prediction_result = query_prediction(DATASET_ID, TABLE_ID)
            return render_template('predictions.html', rows=prediction_result)
        else:
            raise Exception(load_job.error_result)
    except Exception as e:
        error_message = {'event': 'prediction_made', 'status': 'error', 'error': str(e)}
        logging.error(f'Error message: {error_message}')
        publish_message(TOPIC_PATH, error_message)
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
