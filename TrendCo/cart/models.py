from django.db import models
from store.models import Products

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
class CartItems(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product