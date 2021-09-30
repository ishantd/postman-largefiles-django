from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import aggregates
from django.shortcuts import render
from django.conf import settings

from data.models import DatabaseAction, Product, ProductAggregate

def index(request):
    products_list = Product.objects.all().order_by('name')
    aggregate_list = ProductAggregate.objects.all().order_by('-count')[:15].values('name', 'count')
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    prod = settings.DEBUG
    context = {
        'page_obj': page_obj,
        'count' : Product.objects.all().count(),
        'aggregate_table_count' : ProductAggregate.objects.all().count(),
        'aggregate_list': aggregate_list,
        'dbs': list(DatabaseAction.objects.all().values()),
        'in_prod': not(prod)
    }
    return render(request, 'home/index.html', context)

def readme(request):
    return render(request, 'home/readme.html')