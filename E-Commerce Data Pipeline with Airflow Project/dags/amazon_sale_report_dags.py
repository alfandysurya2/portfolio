from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from function.amazon_sale_report_function import F
from datetime import datetime
import pandas as pd
import numpy as np

# Function to Convert Pulled data from Postgres into pandas DataFrame
def convert_to_df(**context):
    data = context['task_instance'].xcom_pull(task_ids='postgre_data_pull')
    df = pd.DataFrame(data)
    return df

# Define the DAG
dag = DAG(
    'amazon_sale_report_data_pipeline_dags',
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
convert_to_dataframe_task = PythonOperator(
    task_id='convert_to_df_task',
    python_callable=convert_to_df,
    provide_context=True,
    dag=dag
)

# Task to standardize data
column_rename_task = PythonOperator(
    task_id='column_rename_task',
    python_callable=F.column_rename,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='convert_to_df') }}"},
    dag=dag
)

# Task to process column
drop_columns = ['promotion_ids', 
                'fulfilled_by', 
                'unnamed_22', 
                'currency', 
                'ship_country']

dropna_columns = ['courier_status', 
                  'ship_city', 
                  'ship_state', 
                  'ship_postal_code']

process_column_task = PythonOperator(
    task_id='column_processing_task',
    python_callable=F.process_column,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='column_standardization') }}",
               'drop_columns': drop_columns,
               'dropna_columns': dropna_columns},
    dag=dag
)

# Task to impute column
x = 'amount'
method = 'mean'

data_imputation_task = PythonOperator(
    task_id='data_imputation_task',
    python_callable=F.data_imputation,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='column_processing_task') }}" ,
               'x':x,
               'method':method},
    dag=dag)

# Task to scale with standard scaler
data_standardization_task = PythonOperator(
    task_id='data_standardization_task',
    python_callable=F.data_standardization,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='data_imputation_task') }}" ,
               'column':'amount'},
    dag=dag)

# Task to categorize column
bins = [0, 450, 900, np.inf]
labels=['Low', 'Medium', 'High']
column='amount'
right=False
column_categorization_task = PythonOperator(
    task_id='data_categorization_task',
    python_callable=F.categorize_column,
    provide_context=True,
    op_kwargs={'df':"{{ task_instance.xcom_pull(task_ids='data_standardization_task') }}" ,
               'column':column,
               'bins':bins,
               'labels':labels,
               'right':right},
    dag=dag)

# Task dependencies
start_task >> \
pull_data_task >> \
convert_to_dataframe_task >> \
column_rename_task >> \
process_column_task >> \
data_imputation_task >> \
data_standardization_task >> \
column_categorization_task




