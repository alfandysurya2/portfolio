##################################
#       Import Dependencies      #
##################################
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

##################################
#  Create Connection and Engine  #
##################################
#Connection Parameter
host = 'localhost'
port = '5432'
database = 'airflow'
user = 'airflow'
password = 'airflow'

connection = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password)
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

##################################
#      Read and Ingest Data      #
##################################
df_list = ['amazon_sale_report', 
           'cloud_warehouse_compersion_chart',
           'expense_iigf',
           'international_sale_report',
           'may_2022',
           'p_l_march_2021',
           'sale_report']

for i in df_list:
    #Get Relative and Absolute Path
    current_dir = os.getcwd()
    relative_path = 'dataset/{}.csv'.format(i)
    absolute_path = os.path.join(current_dir, relative_path)
    print(absolute_path)
    
    #Read CSV
    df = pd.read_csv(absolute_path, low_memory=False)
    df.to_sql(i, engine, if_exists='replace', index=False)
    print(f'data: {i} successfully ingested to database: {database}')

connection.commit()
connection.close()