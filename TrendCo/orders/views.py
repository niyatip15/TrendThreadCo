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
    current_user = request.user
    cart_items = CartItems.objects.filter(user=current_user)
    cart_items_count = cart_items.count()
    
    if cart_items_count <= 0:
        return redirect('store')
    
    total = sum(item.product.product_price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.user = current_user
                order.order_total = grand_total
                order.tax = tax
                order.ip_address = request.META.get("REMOTE_ADDR")
                order.save()
                
                # generate order number
                year = int(datetime.date.today().strftime('%Y'))
                date = int(datetime.date.today().strftime('%d'))
                month = int(datetime.date.today().strftime('%m'))
                day = datetime.date(year, month, date)
                current_date = day.strftime("%Y%m%d")
                order_number = current_date + str(order.id)
                order.order_number = order_number
                order.save()
                
                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total
                }
                print(f"Order saved successfully. Order number: {order_number}")
                return render(request, 'orders/payments.html', context)
            except Exception as e:
                print(f"Error saving order: {str(e)}")
        else:
            print(f"Form validation failed: {form.errors}")
    
    return redirect('checkout')


def payments(request):
    return render(request,'orders/payments.html')