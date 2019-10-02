import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import TableDataQualityOperator

from helpers import SqlDuplicates

'''
Subdag that run data quality checks on the tables in Redshift
'''

def check_table (
        parent_dag_name,
        task_id,
        postgres_conn_id,
        *args, **kwargs):
    
    dag = DAG(
        f"{parent_dag_name}.{task_id}",
        **kwargs
    )

    start_check = DummyOperator(task_id="start_check", dag=dag)

    quality_check_location_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_location_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.location_table",
        dup_sql = SqlDuplicates.deletedup_location_table,
        pri_col=['address'],
    )

    quality_check_opening_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_opening_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.opening_table",
        dup_sql = SqlDuplicates.deletedup_opening_table,
        pri_col=['opening_id'],
    )

    quality_check_business_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_business_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.business_table",
        dup_sql = SqlDuplicates.deletedup_business_table,
        pri_col=['business_table'],
    )

    quality_check_compliment_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_compliment_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.compliment_table",
        dup_sql = SqlDuplicates.deletedup_compliment_table,
        pri_col=['compliment_id'],
)
    quality_check_user_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_user_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.user_table",
        dup_sql = SqlDuplicates.deletedup_user_table,
        pri_col=['user_id', 'compliment_id'],
    )

    quality_check_review_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_review_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.review_table",
        dup_sql = SqlDuplicates.deletedup_review_table,
        pri_col=['review_id', 'user_id', 'business_id'],
    )

    quality_check_tip_table_task = TableDataQualityOperator(
        task_id='Run_data_quality_checks_tip_table_task',
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        table = "public.tip_table",
        dup_sql = SqlDuplicates.deletedup_tip_table,
        pri_col=['tip_id', 'user_id', 'business_id'],
    )

    end_check = DummyOperator(task_id="end_check", dag=dag)

    return dag


