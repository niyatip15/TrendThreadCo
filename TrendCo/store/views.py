from django.shortcuts import render, get_object_or_404,redirect
from store.models import Products,ProductVariation
from product_categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewRatingForm
from django.contrib import messages
# Create your views here.
def store(request,category_slug = None):
    context = {}
    categories = None 
    products = None 
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(product_category = categories, is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Products.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context['products'] = paged_products
    context['product_count'] = product_count
    return render(request, 'store/store.html',context)



def product_detail(request, category_slug, product_slug):
    try:
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Products, product_category=category, slug=product_slug, is_available=True)        
        product_variations = product.variations.all()
        color_variations = product_variations.filter(variation_category='color', is_active=True)     
        size_variations = product_variations.filter(variation_category='size', is_active=True)   
        all_variations = ProductVariation.objects.all()        
        context = {
            'product': product,
            'color_variations': color_variations,
            'size_variations': size_variations,
            'all_variations': product_variations,
        }
        return render(request, 'store/product_detail.html', context)
    except Exception as e:
        print(e,'===================')
        return render(request,{'error_message': str(e)})

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



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # Check if the user already has a review for this product
            review = ReviewRating.objects.get(user=request.user, product_id=product_id)
            form = ReviewRatingForm(request.POST, instance=review)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.product_id = product_id
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            if 'instance' in locals():
                messages.success(request, 'Your review has been updated successfully.')
            else:
                messages.success(request, 'Your review has been submitted successfully.')
        else:
            messages.error(request, 'Failed to submit review. Please check the form.')

    return redirect(url)