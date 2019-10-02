#!/usr/bin/python3
import sys
import pendulum
import logging
import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
#from airflow.operators import (FileDataQualityOperator, FileRemovalOperator)
from airflow.operators import (FileDataQualityOperator)

from helpers import SqlCreate, SqlInsert
from subdag_stage import stage_table
from subdag_load import init_table
from subdag_check import check_table

"""
Main dag file that comprises of the overall flow of data in the pipeline
- Get all file paths with function

If cannot SSH into Vagrant: set VAGRANT_PREFER_SYSTEM_BIN=0
Conda Env: conda activate data-engine
"""

#local_tz = pendulum.timezone("Asia/Singapore")
#start_date = datetime.datetime(year=2019, month=9, day=28, tzinfo=local_tz)
start_date = datetime.datetime.now() - timedelta(minutes=1)

default_args = {
    "owner": "Max",
    "start_date": start_date
}

dag = DAG("dag",
          default_args=default_args,
          description="Load and transform data from Yelp dataset",
          schedule_interval="@once"
        )

# 1. START TASK
start_task = DummyOperator(task_id="start_task", dag=dag)

# 2. DATA QUALITY CHECK OF FileData FILES
check_file_quality_task_id = "check_file_quality_task"
check_file_quality_task = FileDataQualityOperator(
    task_id = check_file_quality_task_id,
    dag = dag,
    save_path = "/udacity_data/data/",
    start_date = start_date,
)


# 3. STAGING DATA FILES
stage_checkin_id = "stage_checkin_task"
subdag_stage_checkin_task = SubDagOperator(
    subdag=stage_table(
        "dag",
        task_id = stage_checkin_id,
        table = "public.staging_checkin",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_STAGING_CHECKIN_TABLE,
        create_sql=SqlCreate.CREATE_STAGING_CHECKIN_TABLE,
        file_path="/udacity_data/data/yelp_academic_dataset_checkin_5000.csv",
        start_date=start_date
    ),
    task_id=stage_checkin_id,
    dag = dag,
)

stage_business_id = "stage_business_task"
subdag_stage_business_task = SubDagOperator(
    subdag=stage_table(
        "dag",
        task_id = stage_business_id,
        table = "public.staging_business",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_STAGING_BUSINESS_TABLE,
        create_sql=SqlCreate.CREATE_STAGING_BUSINESS_TABLE,
        file_path="/udacity_data/data/yelp_academic_dataset_business_5000.csv",
        start_date=start_date
    ),
    task_id=stage_business_id,
    dag = dag,
)


stage_user_id = "stage_user_task"
subdag_stage_user_task = SubDagOperator(
    subdag=stage_table(
        "dag",
        task_id = stage_user_id,
        table = "public.staging_user",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_STAGING_USER_TABLE,
        create_sql=SqlCreate.CREATE_STAGING_USER_TABLE,
        file_path="/udacity_data/data/yelp_academic_dataset_user_5000.json",
        start_date=start_date
    ),
    task_id=stage_user_id,
    dag = dag,
)

stage_review_id = "stage_review_task"
subdag_stage_review_task = SubDagOperator(
    subdag=stage_table(
        "dag",
        task_id = stage_review_id,
        table = "public.staging_review",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_STAGING_REVIEW_TABLE,
        create_sql=SqlCreate.CREATE_STAGING_REVIEW_TABLE,
        file_path="/udacity_data/data/yelp_academic_dataset_review_5000.json",
        start_date=start_date
    ),
    task_id=stage_review_id,
    dag = dag,
)


stage_tip_id = "stage_tip_task"
subdag_stage_tip_task = SubDagOperator(
    subdag=stage_table(
        "dag",
        task_id = stage_tip_id,
        table = "public.staging_tip",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_STAGING_TIP_TABLE,
        create_sql=SqlCreate.CREATE_STAGING_TIP_TABLE,
        file_path="/udacity_data/data/yelp_academic_dataset_tip_5000.csv",
        start_date=start_date
    ),
    task_id=stage_tip_id,
    dag = dag,
)


# 4. LOADING TABLES
location_table_task_id = "location_table_task"
subdag_location_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        location_table_task_id,
        table = "public.location_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_LOCATION_DIM_TABLE,
        create_sql=SqlCreate.CREATE_LOCATION_DIM_TABLE,
        load_sql=SqlInsert.location_table_insert,
        start_date=start_date
    ),
    task_id=location_table_task_id,
    dag=dag,
)

opening_table_task_id = "opening_table_task"
subdag_opening_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        opening_table_task_id,
        table = "public.opening_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_OPENING_DIM_TABLE,
        create_sql=SqlCreate.CREATE_OPENING_DIM_TABLE,
        load_sql=SqlInsert.opening_table_insert,
        start_date=start_date
    ),
    task_id=opening_table_task_id,
    dag=dag,
)

business_table_task_id = "business_table_task"
subdag_business_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        business_table_task_id,
        table = "public.business_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_BUSINESS_DIM_TABLE,
        create_sql=SqlCreate.CREATE_BUSINESS_DIM_TABLE,
        load_sql=SqlInsert.business_table_insert,
        start_date=start_date
    ),
    task_id=business_table_task_id,
    dag=dag,
)

compliment_table_task_id = "compliment_table_task"
subdag_compliment_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        compliment_table_task_id,
        table = "public.compliment_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_COMPLIMENT_DIM_TABLE,
        create_sql=SqlCreate.CREATE_COMPLIMENT_DIM_TABLE,
        load_sql=SqlInsert.compliment_table_insert,
        start_date=start_date
    ),
    task_id=compliment_table_task_id,
    dag=dag,
)

user_table_task_id = "user_table_task"
subdag_user_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        user_table_task_id,
        table = "public.user_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_USER_DIM_TABLE,
        create_sql=SqlCreate.CREATE_USER_DIM_TABLE,
        load_sql=SqlInsert.user_table_insert,
        start_date=start_date
    ),
    task_id=user_table_task_id,
    dag=dag,
)

review_table_task_id = "review_table_task"
subdag_review_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        review_table_task_id,
        table = "public.review_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_REVIEW_FACT_TABLE,
        create_sql=SqlCreate.CREATE_REVIEW_FACT_TABLE,
        load_sql=SqlInsert.review_table_insert,
        fact = True,
        start_date=start_date
    ),
    task_id=review_table_task_id,
    dag=dag,
)

tip_table_task_id = "tip_table_task"
subdag_tip_table_task = SubDagOperator(
    subdag=init_table(
        "dag",
        tip_table_task_id,
        table = "public.tip_table",
        postgres_conn_id = "postgres_default",
        drop_sql=SqlCreate.DROP_TIP_FACT_TABLE,
        create_sql=SqlCreate.CREATE_TIP_FACT_TABLE,
        load_sql=SqlInsert.tip_table_insert,
        fact = True,
        start_date=start_date
    ),
    task_id=tip_table_task_id,
    dag=dag,
)

# 5. DATA QUALITY CHECK
check_table_data_quality_task_id = "table_data_quality_task"
subdag_table_data_quality_task = SubDagOperator(
    subdag=check_table(
        "dag",
        check_table_data_quality_task_id,
        postgres_conn_id = "postgres_default",
        start_date=start_date
    ),
    task_id=check_table_data_quality_task_id,
    dag=dag,
)

# 7. END TASK
end_task = DummyOperator(task_id="end_task", dag=dag)

# WORK FLOW
start_task >> check_file_quality_task
check_file_quality_task >> subdag_stage_checkin_task
check_file_quality_task >> subdag_stage_business_task
check_file_quality_task >> subdag_stage_user_task
check_file_quality_task >> subdag_stage_review_task
check_file_quality_task >> subdag_stage_tip_task
subdag_stage_business_task >> subdag_location_table_task
subdag_stage_business_task >> subdag_opening_table_task
subdag_stage_business_task >> subdag_business_table_task
subdag_stage_checkin_task >> subdag_business_table_task
subdag_stage_user_task >> subdag_compliment_table_task
subdag_stage_user_task >> subdag_user_table_task
subdag_stage_review_task >> subdag_review_table_task
subdag_stage_tip_task >> subdag_tip_table_task
subdag_location_table_task >> subdag_table_data_quality_task
subdag_business_table_task >> subdag_table_data_quality_task
subdag_compliment_table_task >> subdag_table_data_quality_task
subdag_user_table_task >> subdag_table_data_quality_task
subdag_opening_table_task >> subdag_table_data_quality_task
subdag_review_table_task >> subdag_table_data_quality_task
subdag_tip_table_task >> subdag_table_data_quality_task
subdag_table_data_quality_task >> end_task