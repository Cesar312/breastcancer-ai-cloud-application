import os

# Set up GCP credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_account/gcp_20240419_privateKey.json'

# Define BigQuery dataset and table
DATASET_ID = 'bigquery-wk4.uci_bcds'
TABLE_ID = 'raw_mm_ds'

# Path to the CSV file
RAW_FILE_PATH = 'data/raw_data.csv'

# Pub/Sub Topic
TOPIC_PATH = 'projects/bigquery-wk4/topics/bqml-app-topic'

# Project ID for Monitoring
PROJECT_ID = 'bigquery-wk4'
