from django.shortcuts import get_object_or_404, redirect, render
from store.models import Products, ProductVariation
from .models import Cart, CartItems

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
    return cart_id

def add_cart(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    
    selected_variations = []
    
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = ProductVariation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                selected_variations.append(variation)
            except ProductVariation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    is_cart_item_exists = CartItems.objects.filter(cart=cart, product=product, variations__in=selected_variations).exists()

    if is_cart_item_exists:
        cart_item = CartItems.objects.get(cart=cart, product=product, variations__in=selected_variations)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItems.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
        cart_item.variations.add(*selected_variations)
        cart_item.save()

    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        total = sum(cart_item.sub_total() for cart_item in cart_items)
        tax = (2 * total) / 100
        grand_total = total + tax
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total = 0
        tax = 0
        grand_total = 0
        
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

def decrement_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, id=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete() 

    return redirect('cart')


def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')