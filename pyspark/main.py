from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import os
import uuid
import findspark
from tqdm import tqdm
findspark.add_packages('org.postgresql:postgresql:42.2.24')

from io import StringIO
import pandas as pd
import psycopg2

spark = SparkSession.builder.appName('test_new') \
.config('spark.driver.memory','10G') \
.config('jars', '/opt/application/postgresql-42.2.24.jar') \
.config('spark.driver.extraClassPath', 'postgresql-42.2.24.jar') \
.getOrCreate()

os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path /opt/application/postgresql-42.2.24.jar --jars /opt/application/postgresql-42.2.24.jar pyspark-shell'

db_properties={}
db_url = f'jdbc:postgresql://pm-test.cutudajvwdwp.ap-south-1.rds.amazonaws.com:5432/postgres?user=postgres&password=ACXIWFNY4i688J0HfyPo'
db_properties['username'] = "postgres"
db_properties['password'] = "ACXIWFNY4i688J0HfyPo"
db_properties['url'] = db_url
db_properties['driver'] = 'org.postgresql.Driver'

random_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
df_pyspark = spark.read.csv('products.csv', header=True, inferSchema=True).na.drop('any').drop('sku')
df_pyspark = df_pyspark.withColumn('sku', random_udf())
agg_df_pyspark = df_pyspark.groupBy('name').count()
df_pyspark.show()
agg_df_pyspark.show()

# df_pyspark.write.jdbc(url=db_url, table="data_product", mode='overwrite', properties=db_properties)
# agg_df_pyspark.write.jdbc(url=db_url, table="data_product", mode='overwrite', properties=db_properties)
# print("SAVING DATA")
# pd_df = df_pyspark.toPandas()
# print(pd_df)