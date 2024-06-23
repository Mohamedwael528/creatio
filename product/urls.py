from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.orders, name='orders'),
    path('succecful/', views.succecful, name='succecful_orderd'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    
]