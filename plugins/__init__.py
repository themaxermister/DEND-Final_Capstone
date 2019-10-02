from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_plugin"
    operators = [
        operators.FileDataQualityOperator,
        operators.StageToPostgresOperator,
        operators.LoadFactOperator,
        operators.LoadDimensionOperator,
        operators.TableDataQualityOperator
    ]
    helpers = [
        helpers.SqlCreate,
        helpers.SqlInsert,
        helpers.SqlDuplicates,
        helpers.JsonTypes
    ]
