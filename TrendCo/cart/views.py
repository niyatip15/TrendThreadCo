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
        selected_variations = []
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

    is_cart_item_exists = CartItems.objects.filter(cart=cart, product=product).exists()

    if is_cart_item_exists:
        cart_items = CartItems.objects.filter(cart=cart, product=product)
        
        # Check if the current variation combination exists
        existing_variation_list = []
        id = []
        for item in cart_items:
            existing_variations = item.variations.all()
            existing_variation_list.append(list(existing_variations))
            id.append(item.id)

        if selected_variations in existing_variation_list:
            # Increase the quantity of existing item
            index = existing_variation_list.index(selected_variations)
            item_id = id[index]
            item = CartItems.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            # Create a new cart item
            item = CartItems.objects.create(cart=cart, product=product, quantity=1)
            if len(selected_variations) > 0:
                item.variations.clear()
                item.variations.add(*selected_variations)
            item.save()
    else:
        cart_item = CartItems.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(selected_variations) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*selected_variations)
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