from core.models import *
from django.db.models import Min , Max 
from django.contrib import messages

def default(request):
    
    categories =Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price") , Max("price"))
    
    try:
        whishlist = Whishlist.objects.filter(user = request.user)
    except:
        messages.warning("You need to login before accessing whishlist")
        whishlist = 0
    try :
        address = Address.objects.filter(user=request.user).first()
    except :
        address = None

    return {
        "categories" : categories,
        "address":address,
        "whishlist":whishlist,
        "min_max_price":min_max_price,
        "vendors":vendors
    }