from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import aggregates
from django.shortcuts import render

from data.models import DatabaseAction, Product, ProductAggregate

def index(request):
    products_list = Product.objects.all().order_by('name')
    aggregate_list = ProductAggregate.objects.all().order_by('-product_count')[:15].values('name', 'product_count')
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'product_count' : Product.objects.all().count(),
        'aggregate_table_count' : ProductAggregate.objects.all().count(),
        'aggregate_list': aggregate_list,
        'dbs': list(DatabaseAction.objects.all().values())
    }
    return render(request, 'home/index.html', context)