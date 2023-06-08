from django.shortcuts import render
from products.models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def index(request):
    products = Product.objects.all()
    p = Paginator(products,8)
    page_number = request.GET.get('page')
    
    try:
        page=p.page(page_number)
    except PageNotAnInteger:
        page=p.page(1)
    except EmptyPage:
        page=p.page(1)
    
    context = {
        'products': page
    }
    return render(request, 'home/index.html', context)
