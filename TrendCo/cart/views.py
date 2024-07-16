from django.shortcuts import get_object_or_404, redirect, render
from store.models import Products
from . models import Cart, CartItems

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
    return cart_id

def add_cart(request, product_slug):
    color = request.GET['color']
    size = request.GET['size']
    print(f'user selected {color} and {size}')
    product = get_object_or_404(Products, slug=product_slug)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    
    # Check if the product is already in the cart
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()
    
    return redirect('cart')



def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        total = 0
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
        tax = (2 * total) / 100
        grand_total = total + tax
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total = 0
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)