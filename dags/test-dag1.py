from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'himanshi',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

def sayHi(ti,name):
    print(f"Hello {name} from Python opertor")
    ti.xcom_push(key='Name', value=name)

def fetch_name(ti):
    name = ti.xcom_pull(task_ids='t2',key='Name')
    print(f"Name fetched from xcom  {name}")

with DAG(
    dag_id="test_dag1",
    default_args=default_args,
    description="My test dag",
    start_date=datetime(2023,1,19,1),
    schedule_interval='@daily'
) as dag:
    t1 = BashOperator(
        task_id='t1',
        bash_command="echo Hello World!"
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=sayHi,
        op_kwargs={'name': 'Himanshi'}
    )

    t3 = PythonOperator(
        task_id='t3',
        python_callable=fetch_name
    )
    t1 >> t2 
    t1 >> t3
    # >> t2 >>t3