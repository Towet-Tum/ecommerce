from django.contrib import admin

from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'image', 'year', 'maintance', 'fuel_consumption', 'mileage', 'price', 'vin']
    search_fields = ['make', 'model', 'year']
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete', 'transaction_id']
    search_fields = ['customer']
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'date_added']
    search_fields = ['product', 'quantity']
admin.site.register(OrderItem, OrderItemAdmin)

class ShippingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'address', 'city', 'state', 'zipcode', 'date_added']
    search_fields = ['city', 'state']
admin.site.register(ShippingAddress, ShippingAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
admin.site.register(Customer, CustomerAdmin)

admin.site.register(Review)
admin.site.register(ProductVariation)
admin.site.register(ProductInventory)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_url', 'uploaded_at']
admin.site.register(ProductAlbum, AlbumAdmin)