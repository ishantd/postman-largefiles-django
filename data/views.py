from upload.models import FileItem
from django.http import JsonResponse
from django.forms import model_to_dict

from rest_framework.views import APIView

from data.models import Product, ProductAggregate, DatabaseAction
from data.utils import ProcessCSV, start_data_aggregation, start_thread_process
from braces.views import CsrfExemptMixin

class Products(CsrfExemptMixin, APIView):
    
    # def bulk_via_csv(df, columns, model_cls):
    #     """ Inserting 3000 takes 118ms avg """
    #     engine = ExcelImportProcessor._get_sqlalchemy_engine()
    #     connection = engine.raw_connection()
    #     cursor = connection.cursor()
    #     output = StringIO()
    #     df[columns].to_csv(output, sep='\t', header=False, index=False)
    #     output.seek(0)
    #     contents = output.getvalue()
    #     cur = connection.cursor()
    #     cur.copy_from(output, model_cls._meta.db_table, null="", columns=columns)
    #     connection.commit()
    #     cur.close()
    
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('sku', False)
        try:
            product = Product.objects.get(sku=query)
        except:
            return JsonResponse({"status": "ok", "product": False}, status=200)
        return JsonResponse({"status": "ok", "product": model_to_dict(product)}, status=200)
    
    def post(self, request, *args, **kwargs):
        product_sku = request.data.get('product_sku', False)
        name = request.data.get('product_name', False)
        description = request.data.get('product_description', False)
        
        product = Product.objects.get(sku=product_sku)
        if not(product.name == name):
            start_thread_process(start_data_aggregation)
        product.name = name
        product.description = description
        product.save()
        return JsonResponse({"status": "ok", "product": model_to_dict(product)}, status=200)
    
    def delete(self, request, *args, **kwargs):
        product_sku = request.data.get('product_sku', False)
        product = Product.objects.get(sku=product_sku)
        product.delete()
        return JsonResponse({"status": "ok"}, status=200)

class DatabaseActions(CsrfExemptMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            db = DatabaseAction.objects.all().values()
        except:
            return JsonResponse({"status": "ok", "db_actions": False}, status=200)
        return JsonResponse({"status": "ok", "db_actions": list(db)}, status=200)
    
    def post(self, request, *args, **kwargs):
        db_id = request.data.get('db_id', False)
        status = request.data.get('db_status', False)
        
        db = DatabaseAction.objects.get(id=db_id)
        db.status = status
        db.save()
        return JsonResponse({"status": "ok", "db": model_to_dict(db)}, status=200)

class ResetDB(CsrfExemptMixin, APIView):
    def get(self, request, *args, **kwargs):
        DatabaseAction.objects.all().delete()
        Product.objects.all().delete()
        ProductAggregate.objects.all().delete()
        FileItem.objects.all().delete()
        return JsonResponse({"status": "ok"}, status=200)