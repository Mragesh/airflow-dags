from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime.utcnow(),
    'retries': 2
}

dag = DAG(
    dag_id='PHM-ALE-Datalake-Workflow',
    default_args=default_args,
    schedule_interval=timedelta(minutes=120),  # '0 0 * * *',
    dagrun_timeout=timedelta(minutes=119),
)

start = DummyOperator(task_id='start', dag=dag)

fill_datalake = KubernetesPodOperator(
                                      namespace="airflow",
                                      name="datalake-prep",
                                      task_id='prep-datalake',
                                      dag=dag,
                                      default_args=default_args,
                                      image='mragesh/phm-ale-py-code:latest',
                                      cmds=["Python", "-c"],
                                      arguments=["prep-data-lake.py"],
                                      get_logs=True)

stop = DummyOperator(
    task_id='stop',
    dag=dag,
)

start >> fill_datalake
fill_datalake >> stop

if __name__ == "__main__":
    dag.cli()