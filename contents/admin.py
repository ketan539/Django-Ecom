from django.contrib import admin
from .models import *


admin.site.register(Smartphone_Storage)
admin.site.register(Smartphone)
admin.site.register(Smartwatch)
admin.site.register(Smartphone_RAM)
admin.site.register(ProductAttribute)

class ColorAdmin(admin.ModelAdmin):
    list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','smartphone','category','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display=('id','title','image_tag')
admin.site.register(Brand,BrandAdmin)


#Order
class CartOrderAdmin(admin.ModelAdmin):
    list_display=('user','total_amt','paid_status','order_date','order_status')
    list_editable=('paid_status','order_status')
admin.site.register(CartOrder,CartOrderAdmin)


#Order Items
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemAdmin)


#Review
class ReviewAdmin(admin.ModelAdmin):
    list_display=('user','product','review','get_review_rating')
admin.site.register(Review,ReviewAdmin)

#Wishlist
class WishlistAdmin(admin.ModelAdmin):
    list_display=('id','user','product')
admin.site.register(Wishlist,WishlistAdmin)

#Address Book
class AddressAdmin(admin.ModelAdmin):
    list_display=('id','user','address','contact','address_status')
admin.site.register(Address,AddressAdmin)
