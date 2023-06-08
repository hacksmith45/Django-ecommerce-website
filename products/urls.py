from django.urls import path
from .views import *

urlpatterns = [
    path('search/', search_products, name="search"),
    path('<slug>/' , get_product, name="get_product"),
    
]
