import logging
import pandas as pd
import psycopg2

from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers import JsonTypes

class StageToPostgresOperator(BaseOperator):
    ui_color = '#358140'
    
    # JSON SQL
    temp_table_sql = """
        DROP TABLE IF EXISTS stage_json;
        CREATE TABLE IF NOT EXISTS stage_json (data jsonb);
    """

    temp_json_sql ="""
        INSERT INTO stage_json(data)
        VALUES ($${}$$);
    """

    stage_json_sql = """
        INSERT INTO {}
            SELECT {}
            FROM stage_json;
    """
    
    # CSV SQL
    copy_csv_sql = """
        COPY {}
        FROM '{}'                               
        CSV
        DELIMITER ','
        HEADER;
    """
      
    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",                                          
                 table="",                                  
                 file_path="",                                                          
                 *args, **kwargs):

        super(StageToPostgresOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.postgres_conn_id = postgres_conn_id                                                    
        self.file_path = file_path              

    def execute(self, context):                                
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        self.log.info(f"Staging {self.table}")
        self.log.info(self.file_path)
        file_type = (self.file_path).split(".", -1)[-1]
        
        # STAGE JSON FILES TO DATABASE
        if (file_type == "json"):
            # Create temp Json table
            postgres.run(StageToPostgresOperator.temp_table_sql)
            
            # Get columns in Json file
            json_data = pd.read_json(self.file_path, lines=True)
            columns = json_data.columns.tolist() 

            # Fill temp Json table with data from Json file
            with open(self.file_path, 'r') as f:
                for line in f:
                    row = f.readline()
                    row = row.replace("$$", "$")
                    if (row != ""):
                        postgres.run(StageToPostgresOperator.temp_json_sql.format(row))
                            
            # Get data type for data file
            new_col = ""
            if ('user' in self.file_path):
                new_col = JsonTypes.user_types

            elif ('review' in self.file_path):
                new_col = JsonTypes.review_types

            postgres.run(StageToPostgresOperator.stage_json_sql.format(self.table, new_col))
            
            self.log.info(f"{self.table} STAGED")


        # STAGE CSV FILES TO DATABASE
        elif (file_type == "csv"):
            formatted_sql = StageToPostgresOperator.copy_csv_sql.format(
                self.table,
                self.file_path
            )
            postgres.run(formatted_sql)
            logging.info(f"{self.table} STAGED")
        
        else:
            logging.info(f"ERROR STAGING {self.table}: INCORRECT FILE TYPE")
        
        
# The stage operator is expected to be able to load any JSON formatted
# files from 53 to Amazon postgres. The operator creates and runs a SQL
# COPY statement based on the parameters provided. The operator's parameters 
# should specify where in S3 the file is loaded and what is the target table. 

# The parameters should be used to distinguish between JSON file.
# Another important requirement of the stage operator is containing
# a templated field that allows it to load timestamped files from 53 
# based on the execution time and run backfills. 


