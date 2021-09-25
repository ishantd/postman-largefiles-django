from django.urls import path

from data import views

app_name = 'data'

urlpatterns = [
    path('products/',  views.Products.as_view(), name='products'),
]