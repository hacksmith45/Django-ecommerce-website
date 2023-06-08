from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from products.models import *
from django.core.exceptions import ObjectDoesNotExist

def login_page(request):
      if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
         
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
            
        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
        
      return render(request, 'accounts/login.html')




def register_page(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
         
    
      
        user_obj = User.objects.create(first_name = first_name , last_name = last_name, email = email, username = email)
        user_obj.set_password(password)
        user_obj.save()
        
       
        
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
        
    
    
    return render(request, 'accounts/register.html')





def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verifed = True
        user.save()
    except Exception as e:
        return HttpResponse('Invalid Email token')
    
    return redirect('/')


def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    quantity = request.GET.get('quantity', 1)  # Get the selected quantity with a default value of 1
    
    try:
        quantity = int(quantity)
    except ValueError:
        # Handle the case where the 'quantity' parameter is not a valid integer
        # You can raise an error, return an error response, or handle it in a different way based on your requirements
        # For now, let's set a default quantity of 1
        quantity = 1
    
    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    
    cart_item = CartItems.objects.create(cart=cart, product=product, quantity=quantity)  # Save the quantity
    
    if variant:
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
    


def cart(request):
   
    cart_obj = Cart.objects.get(is_paid = False, user = request.user)
    if cart_obj.cart_items.count() == 0:
        return redirect('empty_cart')
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, 'Coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request, f'Coupon expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'Coupon applied.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    context = {'cart': cart_obj,}
    
    return render(request, 'accounts/cart.html', context=context)




def empty_cart(request):
    return render(request, 'accounts/cart-not-found.html')


def checkout(request):
    cart_obj = Cart.objects.get(is_paid=False, user=request.user)
    context = {'cart': cart_obj}
    return render(request, 'accounts/checkout.html',context=context)






def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon Removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))