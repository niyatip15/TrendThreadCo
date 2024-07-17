from django.shortcuts import get_object_or_404, redirect, render
from store.models import Products, ProductVariation
from .models import Cart, CartItems
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
    return cart_id

def add_cart(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    
    selected_variations = []

    # Retrieve selected variations from POST data
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = ProductVariation.objects.filter(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                ).first()  # Choose the first variation if multiple are found
                if variation:
                    selected_variations.append(variation)
            except ProductVariation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    # Check if the cart item with selected variations already exists
    is_cart_item_exists = CartItems.objects.filter(cart=cart, product=product).exists()

    if is_cart_item_exists:
        try:
            cart_item = CartItems.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
        except CartItems.DoesNotExist:
            # Handle case where cart item unexpectedly does not exist
            cart_item = CartItems.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )
            cart_item.variations.add(*selected_variations)
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
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user = request.user,is_active=True)
        else:
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

@login_required(login_url = 'login')
def checkout(request):
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

    return render(request,'store/checkout.html',context)