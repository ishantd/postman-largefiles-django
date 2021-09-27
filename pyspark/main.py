from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import os
import sys
import uuid
import json
import findspark
import getopt, sys
 
try:
    with open(os.path.join('config.json')) as f:
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

DB_CONFIG = get_env_var("DB")
DB_CONFIG = DB_CONFIG["RDS"]

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
        .option("user", "postgres") \
        .option("password", "ACXIWFNY4i688J0HfyPo") \
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
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-p", "--process"):
            p = PySparkProcess()
            products_df = p.read_csv()
            p.write_products_to_db(products_df)
            p.aggregate_and_write_products_to_db(products_df)
             
        elif currentArgument in ("-a", "--aggregate"):
            p = PySparkProcess()
            p.aggregate_and_write_products_to_db(False)
        
        elif currentArgument in ("-l", "-localdb"):
            DB_CONFIG = DB_CONFIG["LOCAL"]            
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))