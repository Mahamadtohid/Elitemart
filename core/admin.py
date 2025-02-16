from django.contrib import admin
from core.models import * 


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display =['user' , 'title' , 'product_image' , 'image' ,'category','vendor','featured' ,'product_status' , 'productid','life','stock_count' , 'type']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display =['title' , 'category_image' ]
    
class VendorAdmin(admin.ModelAdmin):
    list_display =['title' , 'vendor_image' ]
    
class CartsOrderAdmin(admin.ModelAdmin):
    list_display =['user' , 'price' , 'paid_track' ,'date' , 'product_status']
    
class CartsOrderItemAdmin(admin.ModelAdmin):
    list_display =['order' , 'invoice_no' , 'item' ,'image' , 'quantity' , 'price' , 'total']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display =['user' , 'product' , 'review' ,'rating']
    
class WhishlistAdmin(admin.ModelAdmin):
    list_display =['user' , 'product' , 'date']
    
class AddressAdmin(admin.ModelAdmin):
    list_display =['user' , 'address' , 'status']
    
admin.site.register(Product , ProductAdmin)
admin.site.register(Category , CategoryAdmin)
admin.site.register(Vendor , VendorAdmin)
admin.site.register(CartOrder , CartsOrderAdmin)
admin.site.register(CartOrderItems, CartsOrderItemAdmin)
admin.site.register(ProductReview , ProductReviewAdmin)
admin.site.register(Whishlist , WhishlistAdmin)
admin.site.register(Address , AddressAdmin)
