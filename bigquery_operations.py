from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client()

def load_data_to_bigquery(df, dataset_id, table_id):

    # Configure the load job settings
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('Record_Id', 'INTEGER'),
            bigquery.SchemaField('Clump_thickness', 'FLOAT'), 
            bigquery.SchemaField('Uniformity_of_cell_size', 'FLOAT'),
            bigquery.SchemaField('Uniformity_of_cell_shape', 'FLOAT'),
            bigquery.SchemaField('Marginal_adhesion', 'FLOAT'),
            bigquery.SchemaField('Single_epithelial_cell_size', 'FLOAT'),
            bigquery.SchemaField('Bare_nuclei', 'FLOAT'),
            bigquery.SchemaField('Bland_chromatin', 'FLOAT'),
            bigquery.SchemaField('Normal_nucleoli', 'FLOAT'),
            bigquery.SchemaField('Mitoses', 'FLOAT')
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # Load the DataFrame into BigQuery
    load_job = client.load_table_from_dataframe(df, f'{dataset_id}.{table_id}', job_config=job_config)
    load_job.result()

    return load_job

def query_prediction(dataset_id, table_id):

    # Query to make predictions using BigQuery ML model
    prediction_query = f"""
    SELECT
    prediction.label AS predicted_label,
    prediction.prob AS probability,
    *
    FROM ML.PREDICT(MODEL `uci_bcds.dnn_classifier_scaled`,
    (
        SELECT
        Record_Id,
        Clump_thickness AS scaled_Clump_thickness,
        Uniformity_of_cell_size AS scaled_Uniformity_of_cell_size,
        Uniformity_of_cell_shape AS scaled_Uniformity_of_cell_shape,
        Marginal_adhesion AS scaled_Marginal_adhesion,
        Single_epithelial_cell_size AS scaled_Single_epithelial_cell_size,
        Bare_nuclei AS scaled_Bare_nuclei,
        Bland_chromatin AS scaled_Bland_chromatin,
        Normal_nucleoli AS scaled_Normal_nucleoli,
        Mitoses AS scaled_Mitoses
        FROM 
        `bigquery-wk4.uci_bcds.raw_mm_ds`
    ) 
    )
    , UNNEST(predicted_isMalignant_probs) AS PREDICTION;
    """

    # Run the prediction query
    prediction_result = client.query(prediction_query).result()
    return prediction_result
