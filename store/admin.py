# from urllib.parse import urlencode
from django.contrib import admin

from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import  urlencode
# Register your models here.
from . import models


class CollectionAdmin(admin.ModelAdmin):
    list_filter = ("title",)
    list_display = ("title","featured_product",)


admin.site.register(models.Collection,CollectionAdmin)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title","inventory",)
    

admin.site.register(models.Product,ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email","membership",)
    list_editable = ("membership",)
    list_per_page = 10
    list_select_related = ["user"]
    ordering = ["user__first_name","user__last_name"]
    search_fields = ["first_name__istartswith",'last_name__startswith']

admin.site.register(models.Customer,CustomerAdmin)

# class OrderItemAdmin(admin.TabularInline):
class OrderItemAdmin(admin.StackedInline):
    autocomplete_fields = ['product',]
    model = models.Order_Item
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]
    list_display = ("placed_at","payment_status","customer_email")
    list_select_related = ["customer"]
    inlines = [OrderItemAdmin]

    # @admin.display(ordering="customer_email")
    def customer_email(self,Order):

        url = (
            reverse("admin:store_customer_changelist") 
            + '?'
            + urlencode({
                "id" :str(Order.customer.id)
            }))
        return format_html("<a href = '{}'>{}</a>", url ,Order.customer.email) 
        # return format_html("<a href = 'http://google.com'>{}</a>",Order.customer.email) 
        # return Order.customer.email

admin.site.register(models.Order,OrderAdmin)

class Cart(admin.StackedInline):
    model = models.Cart

class CartItem(admin.ModelAdmin):
    inline = [Cart]
    list_display = ["id","cart_id","product","quantity"]

admin.site.register(models.Cart_Item, CartItem)