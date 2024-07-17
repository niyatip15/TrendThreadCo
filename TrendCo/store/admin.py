from django.contrib import admin
from . models import Products, ProductVariation, ReviewRating, ProductGallery
import admin_thumbnails 
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 1
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_category', 'in_stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('product_category', 'in_stock', 'is_available')
    search_fields = ('product_name', 'product_desc')
    prepopulated_fields = {'slug': ('product_name',)} 
    inlines = [ProductGalleryAdmin]
    
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')
     
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
