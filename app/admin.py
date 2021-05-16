from django.contrib import admin
from django.contrib import admin
from .models import Product,Banner,Checkout,Wishlist
 
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['prid','Product_Name', 'original_price','discount','Current_price','Product_display']
class BannerAdmin(admin.ModelAdmin):
    list_display = ['banid','image1', 'image2','image3']
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['check_id','Product_id', 'items','fname', 'lname','email']
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['current_user', 'added_date', 'product']

admin.site.register(Banner,BannerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Checkout,CheckoutAdmin)
admin.site.register(Wishlist,WishlistAdmin)



admin.site.site_header = "Stylox Admin"
admin.site.site_title = "Stylox Admin Panel"
admin.site.index_title = "Welcome To Stylox Admin Panel"