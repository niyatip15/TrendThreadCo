from django.urls import path 
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<slug:product_slug>/', views.add_cart, name='add_cart')
    
]