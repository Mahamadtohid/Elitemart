from django.urls import path , include
from core.views import *
app_name = "core"

urlpatterns = [
    
    # Home Page
    path("", index , name="index"),
    path("products/", products_list_view , name="products-list"),
    path("product/<productid>/", product_detail_view , name="product-detail"),
    
    # Category
    path("category/", category_list_view , name="category-list"),
    path("category/<categoryid>/", category_products_list_view , name="category-products-list"),
    
    # Vendor
    path("vendors/", vendor_list_view , name="vendor-list"),
    path("vendors/<vendorid>/", vendor_details , name="vendor-details"),
    
    #tags
    path("products/tag/<slug:tag_slug>/" , tag_list , name="tags"),
    #add Review
    
    path("ajax-add-review/<productid>/" , ajax_add_review , name="ajax-add-review"),
    
    # Search Products
    path("search/" , search_view , name="search"),
    
    path("filter-products/" , filter_product, name="filter-product"),
    path("add-to-cart/" , add_to_cart , name="add-to-cart"),
    
    #Cart Page url
    path("cart/" , cart_view , name="cart"),
    #delete Items From cart
    path("delete-from-cart/" , delete_item_from_cart , name="delete-from-cart"),
    #Updating cart
    path("update-cart/" , update_cart , name="update-cart"),
    
    path("checkout/" , checkout_view , name="checkout"),
    
    #Payoal Url
    path("paypal/" , include('paypal.standard.ipn.urls')),
    
    #Payment Successful
    path("payment-completed/" , payment_complete_view, name="payment-completed"),
    #payment failed
    path("payment-failed/" , payment_failed_view , name="payment-failed"),
]