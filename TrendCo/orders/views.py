from django.shortcuts import render, redirect
from cart.models import *
from store.models import *
from user_auth.models import *
# Create your views here.
def place_order(request):
    current_user = request.user
    cart_items = CartItems.objects.filter(user = current_user)
    cart_items_count = cart_items.count()
    if cart_items_count <= 0:
        return redirect('store')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
    return render(request, 'orders/place_order.html')