from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','contact_number',
                  'address_line1','address_line2','city','state','country','order_note']