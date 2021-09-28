from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import os
import sys
import uuid
import json
import findspark
import getopt, sys

print(os.getcwd())

try:
    with open('config.json') as f:
        configs = json.loads(f.read())
except:
    configs = None
    print("Couldn't Find config file")

def get_env_var(setting, configs=configs):
 try:
     val = configs[setting]
     if val == 'True':
         val = True
     elif val == 'False':
         val = False
     return val
 except KeyError:
     error_msg = "ImproperlyConfigured: Set {0} environment variable".format(setting)
     print(error_msg)
 except Exception as e:
     print ("some unexpected error occurred!", e)

DB = get_env_var("DB")
DB_CONFIG = DB["RDS"]

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
        self.db_url = f'jdbc:postgresql://{DB_CONFIG["HOST"]}:{DB_CONFIG["PORT"]}/{DB_CONFIG["NAME"]}?user={DB_CONFIG["USER"]}&password={DB_CONFIG["PASSWORD"]}'
        self.db_properties['username'] = DB_CONFIG["USER"]
        self.db_properties['password'] = DB_CONFIG["PASSWORD"]
        self.db_properties['url'] = self.db_url
        self.db_properties['driver'] = 'org.postgresql.Driver'

    def read_csv(self):
        random_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
        self.df_pyspark = self.spark.read.csv('products.csv', header=True, inferSchema=True).na.drop('any').drop('sku')
        self.df_pyspark = self.df_pyspark.withColumn('sku', random_udf())
        return self.df_pyspark
        
        
    def write_products_to_db(self, products_df):
        if not products_df:
            self.df_pyspark.write.jdbc(url=self.db_url, table="data_product", mode='append', properties=self.db_properties)
        else:
            products_df.write.jdbc(url=self.db_url, table="data_product", mode='append', properties=self.db_properties)
            
    def aggregate_and_write_products_to_db(self, products_df):
        products_df = self.spark.read \
        .format("jdbc") \
        .option("url", self.db_url) \
        .option("dbtable", 'data_product') \
        .option("user", DB_CONFIG["USER"]) \
        .option("password", DB_CONFIG["PASSWORD"]) \
        .load()
        self.agg_df_pyspark = products_df.groupBy('name').count()
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
     
    # checking each argument
    for argument in argumentList:
 
        if argument in ("-l", "--localdb"):
            DB_CONFIG = DB["LOCAL"]
        
        if argument in ("-x", "--xdb"):
            DB_CONFIG = DB["PROD"]
        
        elif argument in ("-i", "--interactive"):
            db_type = input("Please choose from local or rds db. \n To make your your choice just enter R for RDS and L for Local \n Note: The RDS database can be monitored using the Django Project.")
            if db_type == 'L' or db_type == 'l':
                DB_CONFIG = DB["LOCAL"]
                
        elif argument in ("-p", "--process"):
            p = PySparkProcess()
            products_df = p.read_csv()
            p.write_products_to_db(products_df)
            p.aggregate_and_write_products_to_db(products_df)
            
        elif argument in ("-a", "--aggregate"):
            p = PySparkProcess()
            p.aggregate_and_write_products_to_db(False)
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))