from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

# Define the DAG
dag = DAG(
    'pull_data_from_postgresql',
    description='DAG to pull data from PostgreSQL',
    schedule_interval='0 0 * * *',  # Run once daily at midnight
    start_date=datetime(2023, 1, 1),
    catchup=False
)

# Define preprocessing function
def process_data(**context):
    data = context['ti'].xcom_pull(task_ids='postgre_data_pull')
    df = pd.DataFrame(data, columns=['column1', 'column2', 'column3'])
    return 


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

process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    provide_context=True,
    dag=dag
)

# Task dependencies
start_task >> pull_data_task




