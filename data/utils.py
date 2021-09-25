from data.models import Product, ProductAggregate
from upload.models import FileItem
from upload.utils import random_string_generator

from django.conf import settings
from django.db.models import Count, aggregates

from tqdm import tqdm
import pandas as pd
import threading

def start_thread_process(target):
    t = threading.Thread(target=target)             
    t.setDaemon(True)
    t.start()

class ProcessCSV:
    
    def __init__(self):
        self.files = FileItem.objects.filter(processed=False)
        self.processed_files = FileItem.objects.filter(processed=True)
        self.pandas_frames = []
    
    def create_pandas_object(self, file):
        return pd.read_csv(file.file.path)
    
    def save_df_into_db(self, df, file):
        products = []
        for row in tqdm(df.itertuples()):
            products.append(
                Product(
                    name=row[1],
                    sku=f'{row[2]}-{random_string_generator(8)}',
                    description=row[3]
                )
            )
        products = Product.objects.bulk_create(objs=products)
        file.processed = True
        file.save()
        return products
    
    def aggregate_data_into_table(self):
        fieldname = 'name'
        product_count = list(Product.objects.all().values(fieldname).order_by(fieldname).annotate(product_count=Count(fieldname)))
        product_count_objects = [ProductAggregate(name=p["name"], product_count=p["product_count"]) for p in product_count]
        ProductAggregate.objects.all().delete()
        new_product_aggregate = ProductAggregate.objects.bulk_create(objs=product_count_objects)
        print("FINISHED AGGREGATING DATA")
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
        


def start_csv_processing():
    p = ProcessCSV()
    p.start_file_processing()
    print("HAHAHHA DONE!!!")
    return True