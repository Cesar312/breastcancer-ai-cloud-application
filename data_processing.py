import pandas as pd
from sklearn.preprocessing import StandardScaler
import xml.etree.ElementTree as ET

def load_and_preprocess_data(file_path, file_type):

    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type == 'xml':
        df = load_xml(file_path)
    elif file_type == 'json':
        df = pd.read_json(file_path)
    else:
        raise ValueError('Invalid file type. Please provide a valid file type: CSV, JSON, or XML.')

    # Select the features for scaling
    features = df.columns.difference(['Record_Id'])
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])

    return df

def load_xml(file_path):
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []

    for record in root.findall('record'):
        record_data = {}
        for child in record:
            record_data[child.tag] = child.text
        data.append(record_data)

    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    return df
