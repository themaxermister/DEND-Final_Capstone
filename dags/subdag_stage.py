#!/usr/bin/env python3
import datetime
import sql
import logging
import psycopg2

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToPostgresOperator)

"""
Subdag that drop, create and loads tables. For reset_dag.py use.
"""

def stage_table (
        parent_dag_name,
        task_id,
        table,
        postgres_conn_id,
        drop_sql,
        create_sql,
        file_path,
        *args, **kwargs):
    
    dag = DAG(
        f"{parent_dag_name}.{task_id}",
        **kwargs
    )

    drop_table = PostgresOperator(
        task_id=f"drop_{table}_table",
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        sql=drop_sql,
    )

    create_table = PostgresOperator(
        task_id=f"create_{table}_table",
        dag=dag,
        postgres_conn_id=postgres_conn_id,
        sql=create_sql,
    )

    load_to_postgres = StageToPostgresOperator(
        task_id=f"load_{table}",
        dag=dag,
        table=table,
        postgres_conn_id=postgres_conn_id,
        file_path=file_path,
    )

    drop_table >> create_table
    create_table >> load_to_postgres
    
    return dag