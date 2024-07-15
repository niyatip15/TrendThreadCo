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
    print("Entering add_cart function")
    
    product = get_object_or_404(Products, slug=product_slug)
    print(f"Product: {product}")
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        print(f"Cart found: {cart}")
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        print(f"New cart created: {cart}")
    
    # Check if the product is already in the cart
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    print(f"Cart Item created: {cart_item}, Created: {created}")
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        print(f"Quantity updated: {cart_item.quantity}")
    else:
        cart_item.quantity = 1
        cart_item.save()
        print(f"New item added to cart with quantity: {cart_item.quantity}")
    
    print("Redirecting to cart")
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