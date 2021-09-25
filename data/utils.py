from data.models import Product

import threading

import time

class ProcessCSV:
    
    def __init__(self):
        self.files = Product.objects.filter(processed=True)
        
    def print_files(self):
        print(self.files)
        time.sleep(5)
        return True
        


def start_csv_processing():
    
    p = ProcessCSV()
    p.print_files()
    return True