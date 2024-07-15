from django.contrib import admin
from . models import Products
# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_category', 'in_stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('product_category', 'in_stock', 'is_available')
    search_fields = ('product_name', 'product_desc')
    prepopulated_fields = {'product_slug': ('product_name',)} 
     
admin.site.register(Products, ProductsAdmin)