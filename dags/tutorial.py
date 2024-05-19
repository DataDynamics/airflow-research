from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from textwrap import dedent
from airflow.models import TaskInstance
from airflow.utils.state import State
from airflow.settings import Session
from airflow.models.taskinstance import TaskInstance
from pprint import pprint

#============== PyCharm Remote Debugging ========================================================:
# PyCharm Remote Debugging 코드로써 Dag에서 PyCharm을 호출하므로 방화벽 설정이 Outbound이어야 함
#
#import pydevd_pycharm
#pydevd_pycharm.settrace('10.0.1.202', port=12345, stdoutToServer=True, stderrToServer=True)
#================================================================================================

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import (
    ExternalPythonOperator,
    PythonOperator,
    PythonVirtualenvOperator,
    is_venv_installed,
)

with DAG(
    'fharenheit', # Dag ID로 DB에 저장되므로 변경되면 다른것으로 인식
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description='A simple tutorial DAG',
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['김병곤']
) as dag:

    def get_previous_success_timestamp(ds=None, **context):
        print("Context에서 값 추출")
        print(context['prev_data_interval_end_success'])
        print((context['prev_data_interval_end_success']).format('YYYY-MM-DD HH:mm:ss.SSS'))
        return context['prev_data_interval_end_success']

    def print_context(ds=None, **context):
        """Print the Airflow context and ds variable from the context."""
        print("::group::All kwargs")
        pprint(context)
        print("::endgroup::")
        print("::group::Context variable ds")
        print(ds)
        print("::endgroup::")
        return "Whatever you return gets printed in the logs"

    def last_execution_date(dag_id: str, task_id: str, n: int):
        session = Session()
        query_val = (
            session.query(TaskInstance)
            .filter(
                TaskInstance.dag_id == dag_id,
                TaskInstance.task_id == task_id,
                TaskInstance.state == State.SUCCESS,
            )
            .order_by(TaskInstance.execution_date.desc())
            .limit(n)
        )
        execution_dates = list(map(lambda ti: ti.execution_date, query_val))
        return execution_dates


    # print(task_instance)

    print("작업을 시작합니다.")

    t2 = PythonOperator(task_id="get_previous_success_timestamp", python_callable=get_previous_success_timestamp)

    print(t2)


    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = PythonOperator(task_id="print_the_context", python_callable=print_context)


    # print(last_execution_date('fharenheit', 'print_date', 1))

    t1 >> t2
