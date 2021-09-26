from django.http import JsonResponse
from django.forms import model_to_dict

from rest_framework.views import APIView

from data.models import Product, ProductAggregate
from data.utils import ProcessCSV, start_thread_process
from braces.views import CsrfExemptMixin

class Products(CsrfExemptMixin, APIView):
    
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
            p = ProcessCSV()
            start_thread_process(p.aggregate_data_into_table())
        product.name = name
        product.description = description
        product.save()
        return JsonResponse({"status": "ok", "product": model_to_dict(product)}, status=200)
    
    def delete(self, request, *args, **kwargs):
        product_sku = request.data.get('product_sku', False)
        product = Product.objects.get(sku=product_sku)
        product.delete()
        return JsonResponse({"status": "ok"}, status=200)