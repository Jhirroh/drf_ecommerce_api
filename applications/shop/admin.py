from django.contrib import admin

from .models import Category, Product, OrderItem, ShippingAddress, Order


class OrderAdmin(admin.ModelAdmin):
    exclude = ('transaction_id',)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Order, OrderAdmin)
