from core.models import *
from django.db.models import Min , Max 

def default(request):
    
    categories =Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price") , Max("price"))
    try :
        address = Address.objects.filter(user=request.user).first()
    except :
        address = None

    return {
        "categories" : categories,
        "address":address,
        "min_max_price":min_max_price,
        "vendors":vendors
    }