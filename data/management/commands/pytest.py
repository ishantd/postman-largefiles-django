from django.core.management.base import BaseCommand
from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from django.conf import settings
import uuid
spark = SparkSession.builder.appName('test_new') \
.config('spark.driver.memory','10G') \
.getOrCreate()
# .config('spark.sql.session.timeZone', 'UTC') \
# .config('spark.ui.showConsoleProgress', True) \
# .config('spark.sql.repl.eagerEval.enabled', True) \

DB_CONFIG = settings.DB_CONFIG

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        db_properties={}
        db_url = f'jdbc:postgresql://{os.environ.get("SQL_HOST", DB_CONFIG["HOST"])}:{os.environ.get("SQL_PORT", DB_CONFIG["PORT"])}/{os.environ.get("SQL_DATABASE", DB_CONFIG["NAME"])}'
        db_properties['username'] = os.environ.get("SQL_USER", DB_CONFIG["USER"])
        db_properties['password'] = os.environ.get("SQL_PASSWORD", DB_CONFIG["PASSWORD"])
        db_properties['url'] = db_url
        db_properties['driver'] = 'org.postgresql.Driver'
        
        random_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
        df_pyspark = spark.read.csv('products.csv', header=True, inferSchema=True).na.drop('any').drop('sku')
        df_pyspark = df_pyspark.withColumn('sku', random_udf())
        agg_df_pyspark = df_pyspark.groupBy('Name').count()
        df_pyspark.write.jdbc(url=db_url,table='product_data',mode='overwrite',properties=db_properties)
        # df_pyspark.show()
