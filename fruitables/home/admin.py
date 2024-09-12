from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem
# Register your models here.
from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    # Add filters for 'status', 'created_at', and 'user'
    list_filter = ('status', 'created_at', 'user', 'payment_status')
    list_display = ( 'user', 'status', 'total', 'payment_status','created_at', 'updated_at')
    readonly_fields = ['created_at', 'updated_at', 'total', 'payment_status']
    fields = ['user', 'status', 'total', 'payment_status','created_at', 'updated_at']
    
    
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)