from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render

from data.models import Product

def index(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'home/index.html', context)