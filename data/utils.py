from data.models import Product, ProductAggregate
from upload.models import FileItem
from upload.utils import random_string_generator

from django.conf import settings
from django.db.models import Count, aggregates

from tqdm import tqdm
import pandas as pd
import threading

class ProcessCSV:
    
    def __init__(self):
        self.files = FileItem.objects.filter(processed=False)
        self.processed_files = FileItem.objects.filter(processed=True)
        self.pandas_frames = []
    
    def create_pandas_object(self, file):
        return pd.read_csv(file.file.path)
    
    def save_df_into_db(self, df, file, index):
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
    
    def aggregate_data_into_table(self, products):
        fieldname = 'name'
        product_count = list(Product.objects.all().values(fieldname).order_by(fieldname).annotate(product_count=Count(fieldname)))
        product_count_objects = [ProductAggregate(name=p["name"], product_count=p["product_count"]) for p in product_count]
        ProductAggregate.objects.all().delete()
        new_product_aggregate = ProductAggregate.objects.bulk_create(objs=product_count_objects)
        return new_product_aggregate
    
    def start_file_processing(self):
        if len(self.processed_files) == 0 and len(self.files) == 1:
            df = self.create_pandas_object(self.files[0])
            saved_to_db = self.save_df_into_db(df, self.files[0], 0)
            aggregated_data = self.aggregate_data_into_table(saved_to_db)
        return True
        


def start_csv_processing():
    p = ProcessCSV()
    p.start_file_processing()
    print("HAHAHHA DONE!!!")
    return True