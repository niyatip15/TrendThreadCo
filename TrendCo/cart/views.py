from django.shortcuts import get_object_or_404, redirect, render
from store.models import Products,ProductVariation
from . models import Cart, CartItems

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
    return cart_id

def add_cart(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    if request.method == 'POST':
        selected_variation = {}
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = ProductVariation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value, product__slug=product_slug)
                selected_variation[key] = variation
            except ProductVariation.DoesNotExist:
                pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})

    if selected_variation:
        cart_item.variations.clear() 
        for key, variation in selected_variation.items():
            cart_item.variations.add(variation)

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