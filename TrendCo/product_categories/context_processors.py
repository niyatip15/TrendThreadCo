from .models import Category

def get_all_category_links(request):
    category_links = Category.objects.all()
    return dict(category_links=category_links)