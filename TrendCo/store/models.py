from django.db import models
from product_categories.models import Category

# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    product_desc = models.TextField(max_length=500,blank=True)
    product_price = models.IntegerField()
    product_images = models.ImageField(upload_to='product_images/')
    in_stock = models.IntegerField()
    is_available = models.BooleanField(default=False)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name