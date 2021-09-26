from data.models import DatabaseAction, Product, ProductAggregate
from upload.models import FileItem
from upload.utils import random_string_generator

from django.conf import settings
from django.db import connection
from django.db.models import Count, aggregates

from sqlalchemy import create_engine
from tqdm import tqdm
import pandas as pd
import threading

import timeit

def start_thread_process(target):
    t = threading.Thread(target=target)             
    t.setDaemon(True)
    t.start()

class ProcessCSV:
    
    def __init__(self):
        self.files = FileItem.objects.filter(processed=False)
        self.processed_files = FileItem.objects.filter(processed=True)
        self.pandas_frames = []
        self.conn_default = create_engine(settings.DB_URI_DEFAULT).connect()
    
    def create_pandas_object(self, file):
        start, stop = None, None
        start = timeit.default_timer()
        db_action = start_db_action("Read CSV into Pandas", "In Progress")
        df = pd.read_csv(file.file.path)
        db_action = modify_db_status(db_action.id, "Completed")
        stop = timeit.default_timer()
        if start and stop:
            time_this_function(start, stop, db_action.id)
        return df
    
    def save_df_into_db(self, df, file):
        start, stop = None, None
        start = timeit.default_timer()
        db_action = start_db_action("Saving Pandas Dataframe in PostgreSQL DB", "In Progress")
        for i in df.index:
            df.at[i, "sku"] = f'{df.at[i, "sku"]}-{random_string_generator(8)}'
        df.to_sql('data_product', if_exists='append',index=False,con=self.conn_default)
        # products = []
        # for row in tqdm(df.itertuples()):
        #     products.append(
        #         Product(
        #             name=row[1],
        #             sku=f'{row[2]}-{random_string_generator(8)}',
        #             description=row[3]
        #         )
        #     )
        # products = Product.objects.bulk_create(objs=products)
        
        file.processed = True
        file.save()
        db_action = modify_db_status(db_action.id, "Completed")
        stop = timeit.default_timer()
        if start and stop:
            time_this_function(start, stop, db_action.id)
        return True
    
    def aggregate_data_into_table(self):
        start, stop = None, None
        start = timeit.default_timer()
        db_action = start_db_action("Aggregating Data in Products Table", "In Progress")
        fieldname = 'name'
        product_count = list(Product.objects.all().values(fieldname).order_by(fieldname).annotate(product_count=Count(fieldname)))
        product_count_objects = [ProductAggregate(name=p["name"], product_count=p["product_count"]) for p in product_count]
        ProductAggregate.objects.all().delete()
        new_product_aggregate = ProductAggregate.objects.bulk_create(objs=product_count_objects)
        db_action = modify_db_status(db_action.id, "Completed")
        stop = timeit.default_timer()
        if start and stop:
            time_this_function(start, stop, db_action.id)
        return new_product_aggregate
    
    def process_all_files(self, file_id):
        file = self.files.get(id=file_id)
        df = self.create_pandas_object(file)
        saved_to_db = self.save_df_into_db(df, file)
        return saved_to_db
    
    def start_file_processing(self):
        [self.process_all_files(f.id) for f in self.files]
        print("STARTING AGGREGATING DATA")
        start_thread_process(self.aggregate_data_into_table)
        return True
        
def start_db_action(name, status):
    return DatabaseAction.objects.create(name=name, status=status)

def modify_db_status(id, status):
    db = DatabaseAction.objects.get(id=id)
    db.status = status
    db.save()
    return db

def finish_db_action(id, time):
    db = DatabaseAction.objects.get(id=id)
    db.time_taken = time
    db.save()
    return db

def time_this_function(start, stop, id):
    execution_time = stop - start
    finish_db_action(id, str(execution_time))
    return True

def start_csv_processing():
    p = ProcessCSV()
    p.start_file_processing()
    print("HAHAHHA DONE!!!")
    return True

def start_data_aggregation():
    p = ProcessCSV()
    p.aggregate_data_into_table()
    print("HAHAHHA DONE!!!")
    return True