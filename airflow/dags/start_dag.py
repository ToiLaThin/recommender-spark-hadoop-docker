import os
import sys
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)
start_date = datetime.now().__add__(timedelta(minutes=.2))

default_args = {
    'owner': 'thinhnd',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

from jobs.extract.extracts import extract_from_csv
from jobs.transform.transform_to_prediction import transform_to_prediction
with DAG('beer_recommender', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    extract_from_csv = PythonOperator(
        task_id='extract_from_csv',
        python_callable=extract_from_csv,
        retries=1,
        retry_delay=timedelta(seconds=5), network_mode='bridge')
    
    transform_to_prediction = PythonOperator(
        task_id='transform_to_prediction',
        python_callable=transform_to_prediction,
        retries=1,
        retry_delay=timedelta(seconds=5))
    
    extract_from_csv >> transform_to_prediction