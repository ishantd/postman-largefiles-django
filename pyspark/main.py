from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import os
import sys
import uuid
import findspark
import getopt, sys
 


findspark.add_packages('org.postgresql:postgresql:42.2.24')


class PySparkProcess:
    
    def __init__(self):
        self.spark = SparkSession.builder.appName('test_new') \
        .config('spark.driver.memory','10G') \
        .config('jars', '/opt/application/postgresql-42.2.24.jar') \
        .config('spark.driver.extraClassPath', 'postgresql-42.2.24.jar') \
        .getOrCreate()

        os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path /opt/application/postgresql-42.2.24.jar --jars /opt/application/postgresql-42.2.24.jar pyspark-shell'

        self.db_properties={}
        self.db_url = f'jdbc:postgresql://pm-test.cutudajvwdwp.ap-south-1.rds.amazonaws.com:5432/postgres?user=postgres&password=ACXIWFNY4i688J0HfyPo'
        self.db_properties['username'] = "postgres"
        self.db_properties['password'] = "ACXIWFNY4i688J0HfyPo"
        self.db_properties['url'] = self.db_url
        self.db_properties['driver'] = 'org.postgresql.Driver'

    def read_csv(self):
        random_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
        self.df_pyspark = self.spark.read.csv('products.csv', header=True, inferSchema=True).na.drop('any').drop('sku')
        self.df_pyspark = self.df_pyspark.withColumn('sku', random_udf())
        
    def write_products_to_db(self):
        self.df_pyspark.write.jdbc(url=self.db_url, table="data_product", mode='append', properties=self.db_properties)
     
    def aggregate_and_write_products_to_db(self):
        self.producuts_df = self.spark.read \
        .format("jdbc") \
        .option("url", self.db_url) \
        .option("dbtable", 'data_product') \
        .option("user", "postgres") \
        .option("password", "ACXIWFNY4i688J0HfyPo") \
        .load()
        self.agg_df_pyspark = self.producuts_df.groupBy('name').count()
        self.agg_df_pyspark.write.jdbc(url=self.db_url, table="data_productaggregate", mode='overwrite', properties=self.db_properties)

 
# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
 
# Options
options = "pa:"
 
# Long options
long_options = ["process", "aggregate"]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-p", "--process"):
            p = PySparkProcess()
            p.read_csv()
            p.write_products_to_db()
            p.aggregate_and_write_products_to_db()
             
        elif currentArgument in ("-a", "--aggregate"):
            p = PySparkProcess()
            p.aggregate_and_write_products_to_db()
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))