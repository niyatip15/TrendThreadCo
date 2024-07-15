from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Products
from . models import Cart,CartItems
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    try:
        cart_item = CartItems.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
    cart_item.save()
    return redirect('cart')


def cart(request,total=0,quantity=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items' : cart_items
        }
        
    return render(request, 'store/cart.html',context)