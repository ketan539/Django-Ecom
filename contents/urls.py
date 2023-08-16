from . import views 
from django.urls import path,include
from .views import *

urlpatterns = [
path('home',views.home,name='home'),
path('search',views.search,name='search'),
path('',views.home,name='home'),
path('category_list',views.category_list,name='category_list'),
path('brand_list',views.brand_list,name='brand_list'),
path('smartphone#list/',views.smartphone_list,name='smartphone_list'),
path('smartwatch_list',views.smartwatch_list,name='smartwatch_list'),
path('product_list',views.product_list,name='product_list'),
path('single_brand_list/<str:cat>',views.single_brand_list,name='single_brand_list'),
path('single_product_detail/<int:id>',views.single_product_detail,name='single_product_detail'),
path('filter-data',views.filter_data,name='filter-data'),
path('load-more-data',views.load_more_data,name='load-more-data'),
path('add-to-cart',views.add_to_cart,name='add-to-cart'),
path('delete-from-cart',views.delete_from_cart,name='delete-from-cart'),
path('update_from_cart',views.update_from_cart,name='update_from_cart'),
path('cart',views.cart_list,name='cart'),
path('accounts/signup',signup.as_view(),name='signup'),
path('checkout',views.checkout,name='checkout'),
path('paypal/',include('paypal.standard.ipn.urls')),
# path('process_payment/',views.process_payment,name='process_payment'),
path('payment_done/',views.payment_done,name='payment_done'),
path('payment_cancelled/',views.payment_cancelled,name='payment_cancelle d'),
path('save_review/<int:pid>',views.save_review,name='save_review'),
path('user/edit_profile',views.edit_profile,name='edit_profile'),
path('user/my_orders',views.my_orders,name='my_orders'),
path('user/dashboard',views.dashboard,name='dashboard'),
path('user/order_items/<int:id>',views.order_items,name='order_items'),
path('add_wishlist',views.add_wishlist,name='add_wishlist'),
path('my_wishlist',views.my_wishlist,name='my_wishlist'),
path('my_reviews',views.my_reviews,name='my_reviews'),
path('my_address',views.my_address,name='my_address'),
path('add_address',views.add_address,name='add_address'),
path('activate_address',views.activate_address,name='activate_address'),
path('update_address/<int:id>',views.update_address,name='update_address'),
path('password/',PasswordEditView.as_view()),
path('PasswordChanged',views.PasswordChanged,name='password_changed'),
# path('password_reset',views.password_reset,name='password_reset'),



]