from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from accounts.models import *
from django.http import JsonResponse

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}
        
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
        
        return render(request, 'product/product.html', context=context) 
    
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred") 
    
    

    
    
def search_products(request):
    query = request.GET.get('query', '')
    
    products = Product.objects.filter(product_name__icontains=query)
    
    return render(request, 'product/search.html', {'products': products, 'query':query})


