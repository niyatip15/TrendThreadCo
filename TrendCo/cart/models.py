from django.db import models
from store.models import Products,ProductVariation
from user_auth.models import CustomUser

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
class CartItems(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    variations = models.ManyToManyField(ProductVariation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.product_price * self.quantity
    
    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"