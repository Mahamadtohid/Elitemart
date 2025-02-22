from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse , JsonResponse
from core.models import *
from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag
from django.db.models import Count , Aggregate , Avg
from core.forms import *
from django.template.loader import render_to_string
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from datetime import date
from userauth.models import Profile
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth


def index(request):
    products = Product.objects.filter(product_status="published" , featured=True).order_by("-id")
    
    
    context = {
        "products" : products,
        
    }
    return render(request, "core/index.html" , context)


def products_list_view(request):
    products = Product.objects.filter(product_status="published" , featured=True).order_by("-id")
    
    
    context = {
        "products" : products,
        
    }
    return render(request, "core/products-list.html" , context)

def category_list_view(request):
    
    categories = Category.objects.all()
    # categories = Category.objects.all().annotate(prosuct_count = Count("products"))
    
    context = {
        
        "categories" : categories
        
    }
    
    return render(request, "core/category-list.html" , context)

def category_products_list_view(request, categoryid):
    category = Category.objects.get(categoryid = categoryid)
    products = Product.objects.filter(category = category , product_status="published")
    
    
    context = {
        "category" : category,
        "products" :products
    }
    
    return render(request , "core/category-products-list.html" , context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors" : vendors
    }
    return render(request , "core/vendor-list.html" , context)


def vendor_details(request , vendorid):
    vendor = Vendor.objects.get(vendorid=vendorid)
    products = Product.objects.filter(vendor = vendor , product_status="published")
    context = {
        "vendor" : vendor,
        "products" : products
    }
    return render(request , "core/vendor-details.html" , context)

def product_detail_view(request , productid):
    product = Product.objects.get(productid = productid)
    reviews = ProductReview.objects.filter(product = product).order_by("-date")
    average_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))
    product_images = product.product_images.all()
    
    products = Product.objects.filter(category = product.category)
    # .exclude(productid = productid)
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count =ProductReview.objects.filter(user=request.user , product=product).count()
        
        if user_review_count > 0:
            make_review = False
    
    # Product review Form
    review_form = productReviewForm()
    context = {
        "product" : product,
        "review_form":review_form,
        'make_review':make_review,
        "product_images":product_images,
        "products" : products,
        "average_rating":average_rating,
        "reviews":reviews,
    }
    
    return render(request , "core/product-detail.html" , context)


def tag_list(request , tag_slug = None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None
    
    if tag_slug :
        tag = get_object_or_404(Tag , slug=tag_slug)
        products = products.filter(tag__in=[tag])  
    
    context = {
        "products":products,
        "tag":tag
    }
    return render(request , "core/tag.html" , context)


def ajax_add_review(request , productid):
    product = Product.objects.get(productid = productid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating' : request.POST['rating'],
    }
    
    average_review = ProductReview.objects.filter(product = product).aggregate(rating =Avg('rating'))
    
    return JsonResponse(
        {
        'bool': True,
        'context':context,
        'average_review':average_review,
        }
    )
   
   
def search_view(request):
    query = request.GET.get("query")
    
    products = Product.objects.filter(title__icontains="Shoe").order_by("-date")
    # products = Product.objects.annotate(
    #         similarity=TrigramSimilarity('title', query)
    #     ).filter(similarity__gt=0.3).order_by('-similarity')

    
    context = {
        "products" : products,
        "query" : query
    } 
    print(Product.objects.all())  # Check if there are any products at all

    print(Product.objects.filter(title__icontains="Shoe"))
    
    return render(request , "core/search.html" , context)


def filter_product(request):
    categories = request.GET.getlist("category[]", [])
    vendors = request.GET.getlist("vendor[]", [])
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    

    # Fetch only published products
    products = Product.objects.filter(product_status="published").order_by("-id")
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    # Apply category filtering if categories are provided
    if categories:
        products = products.filter(category__id__in=categories)

    # Apply vendor filtering if vendors are provided
    if vendors:
        products = products.filter(vendor__id__in=vendors)

    # Render filtered products into an HTML template
    data = render_to_string("core/async/product-list.html", {"products": products}, request=request)

    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_products = {}
    cart_products[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'quantity' : request.GET['quantity'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid']
        
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])] ['quantity'] = int(cart_products[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_products)
            request.session['cart_data_obj']= cart_data
            
    else:
        request.session['cart_data_obj'] = cart_products
        
    return JsonResponse({"data":request.session['cart_data_obj'] , "totalcartitems": len(request.session['cart_data_obj'])})

 
 
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['price']) * int(item['quantity'])
        return render(request , 'core/cart.html' , {"cart_data":request.session['cart_data_obj'] , "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request ,"Your cart is Empty")
        return redirect("core:index")
    
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0       
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['price']) * int(item['quantity'])
            
    context = render_to_string("core/async/cart-list.html" , ({"cart_data":request.session['cart_data_obj'] , "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount}))
    
    return JsonResponse({"data":context , "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_quantity = request.GET['quantity']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            # del request.session['cart_data_obj'][product_id]
            cart_data[str(request.GET['id'])] ['quantity'] = product_quantity
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0       
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['price']) * int(item['quantity'])
            
    context = render_to_string("core/async/cart-list.html" , ({"cart_data":request.session['cart_data_obj'] , "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount}))
    
    return JsonResponse({"data":context , "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount})

def convert_inr_to_usd(cart_total_amount):
    exchange_rate = 86  # Fixed exchange rate (1 USD = 82 INR)
    amount_in_usd = cart_total_amount / exchange_rate  # Convert INR to USD
    return '%.2f' % amount_in_usd


# import stripe
# def create_checkout_session(request , oid):
    order = CartOrder.objects.get(oid = oid)
    stripe.api_key = settings.STRIPE_SECRETE_KEY
    
    checkout_session = stripe.checkout.Session.create(
        customer_email = order.email,
        payment_method_type = ['card'],
        line_items = [
            {
                'price_data':{
                    'currency': 'INR',
                    'product_data':{
                        'name': order.full_name,
                        
                    },
                    'unit_amount': int(order.price * 1000)
                },
                'quantity': 1
            }
        ],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse('core:payment-completed' , args=[order.oid])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('core:payment-failed'))
    )
        
    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()
    
    
@login_required
def checkout_view(request):
    cart_total_amount = 0    
    total_amount = 0   
    
    # if request.method == "POST":
    #     code = request.POST.get("code")
    #     coupon = Coupon.objects.filter(code = code , active=True).first()
    #     if coupon in order.coupons.all():
    #         messages.warning(request,"Coupon Already Activated..")
    #         return redirect("core:checkout" , order.oid)
    #     else:
    #         discount = order.price * coupon.discount / 100
            # order.coupons.add(coupon)
            # order.price -= discount
            # order.save += discount
            #order.save()
    #         messages.success(request,"Coupon Activated..")
    #         return redirect("core:checkout" , order.oid)
    # else:
    #     messages.error(request,"Coupon Does Not Exist..")
    #     return redirect("core:checkout" , order.oid)
    # Checking cart_data_obj still exist in session or not
    if 'cart_data_obj' in request.session:
        #Getting total Ammount for the Paypal
        for product_id , item in request.session['cart_data_obj'].items():
            total_amount += float(item['price']) * int(item['quantity'])
        
        #creating order Objects
        order =CartOrder.objects.create(
            user = request.user,
            price = total_amount,
            
        )
        
        #Getting total Ammount for the cart
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['price']) * int(item['quantity'])
            
            cart_order_item = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-"+str(order.id),
                item = item['title'],
                image = item['image'],
                quantity = item['quantity'],
                price = item['price'],
                total = int(item['quantity']) * float(item['price'])
                
            )
        amount_in_usd = convert_inr_to_usd(cart_total_amount)

            
    
    host = request.get_host()
    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount' : amount_in_usd,
        'item_name':"Order-Item-No-"+str(order.id),
        'invoice':"INVOICE_Num-2"+str(order.id),
        'currency_code':"USD",
        'notify_url': f"http://{host}{reverse('core:paypal-ipn')}",
        'return_url': f"http://{host}{reverse('core:payment-completed')}",
        'cancel_url': f"http://{host}{reverse('core:payment-failed')}",
        
        
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    cart_total_amount = 0      
    # active_address = Address.objects.get(user=request.user, status=True) 
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['price']) * int(item['quantity'])
        # return render(request , "core/checkout.html")
        
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
        messages.warning(request , "Multiple addresses , Only one shiuld be activated")  
        active_address = None
    
    return render(request , 'core/checkout.html' , {"cart_data":request.session['cart_data_obj'] ,"product_id":product_id,"totalcartitems": len(request.session['cart_data_obj']) ,'cart_total_amount':cart_total_amount , 'paypal_payment_button':paypal_payment_button ,"active_address":active_address})

@login_required
def payment_complete_view(request):
    cart_total_amount = 0 
    today = date.today()      
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['price']) * int(item['quantity'])
    # return render(request , 'core/payment-complete.html')
        
    return render(request , 'core/payment-complete.html' , {"cart_data":request.session['cart_data_obj'] , "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount , 'today':today})

    
    
@login_required
def payment_failed_view(request):
    return render(request , 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user = request.user).order_by("-id")
    address = Address.objects.filter(user = request.user)
    profile = Profile.objects.get(user = request.user)
    order_list = CartOrder.objects.annotate(month = ExtractMonth("date")).values("month").annotate(count = Count("id")).values("month" , "count")
    month = []
    total_order = []
    
    for order in order_list:
        month.append(calendar.month_name[order['month']])
        total_order.append(order['count'])
    for order in orders :
        amount_in_usd = convert_inr_to_usd(order.price)
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        
        new_address = Address.objects.create(
            user = request.user,
            address = address,
            # mobile = mobile
        )
        messages.success(request, f"Hey {request.user} Address Added Successfully")
        return redirect("core:dashboard")
    
    context = {
        "profile":profile,
        "orders":orders,
        "order_list":order_list,
        "month":month,
        "total_order":total_order,
        "amount_in_usd":amount_in_usd,
        'address':address,
    }
    return render(request , 'core/customer-dashboard.html' , context)

def order_detail(request , id):
    order=CartOrder.objects.get(user = request.user , id = id)
    products = CartOrderItems.objects.filter(order = order)   
    for product in products :
        amount_in_usd = convert_inr_to_usd(order.price)
    context = {
        "products":products,
        "amount_in_usd":amount_in_usd,
    }  
    
    return render(request , 'core/order-detail.html' , context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id = id).update(status=True)
    return JsonResponse({"boolean":True})
@login_required
def add_to_whishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id = product_id)
    
    context = {
        
    }
    whishlist_count = Whishlist.objects.filter(user = request.user , product = product).count()
    
    if whishlist_count > 0:
        context ={
            'bool':True
        }
    else:
        new_whishlist = Whishlist.objects.create(
            user = request.user,
            product=product,
        )
        context = {
            "bool":True
        }
    
    return JsonResponse(context)
    # return render(request , 'core/add-to-whishlist.html' , context)

@login_required 
def wishlist_view(request):
    # try:
    wishlist = Whishlist.objects.all()
    # except :
    #     wishlist = None
    context = {
        "wishlist":wishlist
    }
    
    return render(request , "core/wishlist.html" , context)

def remove_wishliat(request):
    productid = request.GET['id']
    wishlist = Whishlist.objects.filter(user = request.user)
    
    product = Whishlist.objects.get(id = productid)
    product.delete()
    
    context={
        "bool":True,
        "wishlist":wishlist
    }
    wishlist_json = serializers.serialize("json" , wishlist)
    
    data = render_to_string("core/async/wishlist-list.html" , context)
    return JsonResponse({"data":data , "wishlist":wishlist_json})


def product(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    
    context = {
        "all_products":all_products,
        "all_categories":all_categories
    }
    
    return render(request , "product.html" , context)

def contactus(request):
    return render(request , "core/contactus.html")