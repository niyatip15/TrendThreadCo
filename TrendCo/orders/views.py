from django.shortcuts import render, redirect
from cart.models import *
from store.models import *
from user_auth.models import *
from .forms import OrderForm
from .models import *
import datetime
from datetime import datetime
# Create your views here.
import logging
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItems
from .forms import OrderForm
import datetime

@login_required
def place_order(request):
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    current_user = request.user
    cart_items = CartItems.objects.filter(user=current_user)
    cart_items_count = cart_items.count()
    
    if cart_items_count <= 0:
        return redirect('store')
    
    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                data = Order()
                data = form.save(commit=False) 
                data.user = current_user
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.contact_number = form.cleaned_data['contact_number']
                data.email = form.cleaned_data['email']
                data.address_line1 = form.cleaned_data['address_line1']
                data.address_line2 = form.cleaned_data['address_line2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.order_note = form.cleaned_data['order_note']
                data.order_total = grand_total
                data.tax = tax
                data.ip_address = request.META.get("REMOTE_ADDR")
                data.save()
                
                # generate order number
                year = int(datetime.date.today().strftime('%Y'))
                date = int(datetime.date.today().strftime('%d'))
                month = int(datetime.date.today().strftime('%m'))
                day = datetime.date(year, month, date)
                current_date = day.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                
                print(f"Order saved successfully. Order number: {order_number}")
                return redirect('checkout')
            except Exception as e:
                print(f"Error saving order: {str(e)}")
        else:
            print(f"Form validation failed: {form.errors}")
    
    return redirect('checkout')