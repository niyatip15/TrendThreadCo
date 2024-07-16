from django.shortcuts import render, get_object_or_404, HttpResponse
from store.models import Products
from product_categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def store(request,category_slug = None):
    context = {}
    categories = None 
    products = None 
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(product_category = categories, is_available=True)
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Products.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products,5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context['products'] = paged_products
    context['product_count'] = product_count
    return render(request, 'store/store.html',context)



def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Products, product_category=category, slug=product_slug, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Products.objects.order_by('-created_date').filter(Q(product_desc__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
