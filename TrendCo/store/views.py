from django.shortcuts import render, get_object_or_404
from store.models import Products
from product_categories.models import Category
# Create your views here.
def store(request,slug = None):
    context = {}
    categories = None 
    products = None 
    if slug != None:
        categories = get_object_or_404(Category,slug=slug)
        products = Products.objects.filter(product_category = categories, is_available=True)
        product_count = products.count()
    else:
        products = Products.objects.filter(is_available=True)
        product_count = products.count()
    context['products'] = products
    context['product_count'] = product_count
    return render(request, 'store/store.html',context)