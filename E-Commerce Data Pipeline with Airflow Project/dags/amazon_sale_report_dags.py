from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from plugins import amazon_sale_report_function as sr
import pandas as pd

# Function to Convert Pulled data from Postgres into pandas DataFrame
def convert_to_df(**context):
    data = context['task_instance'].xcom_pull(task_ids='postgre_data_pull')
    df = pd.DataFrame(data)
    return df

# Define the DAG
dag = DAG(
    'pull_data_from_postgresql',
    description='DAG to pull data from PostgreSQL',
    schedule_interval='0 0 * * *',  # Run once daily at midnight
    start_date=datetime(2023, 1, 1),
    catchup=False
)

# Define tasks
start_task = EmptyOperator(task_id='start_task', dag=dag)

# Task to pull data from PostgreSQL
pull_data_task = PostgresOperator(
    task_id='postgre_data_pull',
    sql="SELECT * FROM amazon_sale_report",
    postgres_conn_id='postgres_connection_id',  # Specify your PostgreSQL connection ID
    autocommit=True,
    dag=dag
)

# Task to convert pulled data from PostgreSQL to Pandas Dataframe
convert_to_df_task = PythonOperator(
    task_id='convert_to_df',
    python_callable=convert_to_df,
    dag=dag
)

column_standardization = PythonOperator(
    task_id='column_standardization_task',
    python_callable=sr.column_standardization,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='postgre_data_pull') }}"},
    dag=dag
)

process_column = PythonOperator(
    task_id='column_processing_task',
    python_callable=sr.process_column,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='postgre_data_pull') }}"},
    dag=dag
)

# Task dependencies
start_task >> pull_data_task >> column_standardization




