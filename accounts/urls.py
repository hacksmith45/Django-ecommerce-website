from django.urls import include, path
from .views import *
# from products.views import 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('activate/<email_token>/', activate_email, name="activate_email"),
    path('cart/', cart , name="cart"),
    path('add-to-cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('remove-cart/<cart_item_uid>/', remove_cart, name="remove_cart"),
    path('remove-coupon/<cart_id>/', remove_coupon, name="remove_coupon"),
    path('empty-cart/', empty_cart, name="empty_cart"),
    path('checkout/', checkout, name="checkout"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    
]
