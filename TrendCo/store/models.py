from django.db import models
from product_categories.models import Category
from user_auth.models import CustomUser
from django.db.models import Avg,Count
# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    product_desc = models.TextField(max_length=500,blank=True)
    product_price = models.IntegerField()
    product_images = models.ImageField(upload_to='product_images/')
    in_stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product = self, status = True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def __str__(self):
        return self.product_name
    
    
    
variation_category_choice = (
    ('color','color'),
    ('size','size'),
)
class ProductVariation(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=200, choices= variation_category_choice)
    variation_value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.variation_value
    
    
class ReviewRating(models.Model):
    product  = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review = models.TextField(max_length=500,blank=True)
    subject = models.CharField(max_length=100, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.review
    
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/', max_length=255)
    
    def __str__(self):
        return self.product.product_name