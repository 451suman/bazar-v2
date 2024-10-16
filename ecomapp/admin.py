from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([ Category, Cart, CartProduct])
from django.contrib import admin
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "marked_price", "selling_price", "warranty", "return_policy", "thumbnail")
    list_per_page = 5
    ordering = ("-id",) 
    search_fields = ["title", "category__name", "return_policy"]
    list_filter = ("category", "warranty")

    def thumbnail(self, obj):
        return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
    thumbnail.short_description = 'Image'

admin.site.register(Product, ProductAdmin)


from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',  
        'ordered_by',
        'email',
        'shipping_address',
        'mobile',
        'subtotal',  
        'discount',
        'total',
        'order_status',
        'created_at',  
    )
    list_filter = ('order_status', 'created_at')  
    search_fields = ('ordered_by', 'email', 'shipping_address')  
    ordering = ['-created_at']
    date_hierarchy = 'created_at'  
   
admin.site.register(Order, OrderAdmin)



class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "address", "mobile")
    search_fields = ("full_name", "mobile")  

admin.site.register(Customer, CustomerAdmin)

class AdminAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name",  "mobile","image")
    search_fields = ("full_name", "mobile")  

admin.site.register(Admin, AdminAdmin)