from django.contrib import admin
from .models import Payments, Order, OrderItems

# Register your models here.

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('payment_id', 'user__username', 'user__email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'order_total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email')

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'product_variation', 'color', 'size', 'quantity', 'ordered', 'created_at')
    list_filter = ('ordered', 'created_at')
    search_fields = ('order__order_number', 'product__product_name')
