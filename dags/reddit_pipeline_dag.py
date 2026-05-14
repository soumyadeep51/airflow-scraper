from reddit_ingestion import fetch_and_save
from transform import transform_data
from load import load_data_to_db
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
with DAG(dag_id="reddit_etl_pipeline",start_date=datetime(2026, 5, 14),schedule_interval="@daily",catchup=False) as dag:
    fetch_and_save_task=PythonOperator(task_id="fetch_and_save",python_callable=fetch_and_save)
    transform_data_task=PythonOperator(task_id="transform_data",python_callable=transform_data)
    load_data_to_db_task=PythonOperator(task_id="load_data_to_db",python_callable=load_data_to_db)
    fetch_and_save_task >> transform_data_task >> load_data_to_db_task
    