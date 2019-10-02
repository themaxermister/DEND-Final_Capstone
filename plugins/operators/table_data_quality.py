import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class TableDataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 table="",
                 dup_sql="",
                 pri_col=[],
                 *args, **kwargs):

        super(TableDataQualityOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.dup_sql = dup_sql
        self.pri_col = pri_col

    def execute(self, context):
        postgres_hook = PostgresHook(self.postgres_conn_id)
        records = postgres_hook.get_records(f"SELECT COUNT(*) FROM {self.table}")

    ## 1. HAVE ROWS IN TABLE
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Data quality check failed. {self.table} returned no results")
        num_records = records[0][0]

        if num_records < 1:
            raise ValueError(f"Data quality check failed. {self.table} contained 0 rows")
        logging.info(f"Data quality on table {self.table} check passed with {records[0][0]} records")

    ## 2. REMOVE EXACT DUPLICATES IN TABLE
        postgres_hook.run(self.dup_sql)
        self.log.info(f"DUPLICATES REMOVED FROM {self.table}")
    
    ## 3. REMOVE NULL PRIMARY VALUES
        for col in self.pri_col:
            postgres_hook.run(f"DELETE FROM {self.table} WHERE {col} IS NULL;")


# The final operator to create is the data quality operator, which is used to run checks on the data itself.
# The operator's main functionality is to receive one or more SQL based test cases along with the expected 
# results and execute the tests. For each the test. the test result and expected result needs to be checked 
# and if there is no match, the operator should raise an exception and the task should retry and fail eventually. 

# For example one test could be a SQL statement that checks if certain column contains NULL values by counting all
# the rows that have NULL in the column. We do not want to have any NULLs so expected result would be O and the test 
# would compare the SQL statement's outcome to the expected result.
