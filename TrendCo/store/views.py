from django.shortcuts import render
from store.models import Products
# Create your views here.
def store(request):
    context = {}
    products = Products.objects.filter(is_available=True)
    product_count = products.count()
    context['products'] = products
    context['product_count'] = product_count
    return render(request, 'store/store.html',context)