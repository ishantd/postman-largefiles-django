from data.models import Product
from upload.models import FileItem
from upload.utils import random_string_generator

from django.conf import settings

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
    
    def start_file_processing(self):
        if len(self.processed_files) == 0 and len(self.files) == 1:
            df = self.create_pandas_object(self.files[0])
            saved_to_db = self.save_df_into_db(df, self.files[0], 0)
        return True
        


def start_csv_processing():
    p = ProcessCSV()
    p.start_file_processing()
    return True