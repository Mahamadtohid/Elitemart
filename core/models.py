from django.db import models
from shortuuid.django_fields import ShortUUIDField #shortuuid.django_fields
from django.utils.html import mark_safe 
from userauth.models import User
# from pyexpat import model
# from unicodedata import decimal
# from email.policy import default
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("process", "Processing"),
    ("process", "Shipped"),
    ("process", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATINGS = (
    (1, "★☆☆☆☆"),
    (2 ,"★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

def user_directory_path(instance , filname):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filname)
class Category(models.Model):
    categoryid = ShortUUIDField(unique=True ,length = 10, max_length=20 ,prefix="cat" , alphabet="abcdefgh12345")
    title = models.CharField(max_length=100 , default="products")
    image = models.ImageField(upload_to='category' , default="category.jpg")
    
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    vendorid = ShortUUIDField(unique=True , length = 10 , max_length=20 ,prefix="cat" , alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path , default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path , default="vendor.jpg")
    # description = models.TextField(null=True , blank=True  , default="I am a vendor")
    description = RichTextUploadingField(null=True , blank=True  , default="I am a vendor")
    
    address = models.CharField(max_length=100 , default = "12 Main Street")
    contact = models.CharField(max_length=20 , default = "+91 123(456) 789")
    chat_resp_time = models.CharField(max_length=100 , default="100")
    shipping_on_time = models.CharField(max_length=100 , default="100")
    authentic_rating = models.CharField(max_length=100 , default="1")
    days_return = models.CharField(max_length=100 , default="1")
    warrenty_period = models.CharField(max_length=100 , default="1")
    date = models.DateTimeField(auto_now_add=True , null=True , blank = True)
    
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    productid = ShortUUIDField(unique=True , length = 10 , max_length=20 , alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True , related_name="category")
    vendor = models.ForeignKey(Vendor , on_delete=models.SET_NULL , null=True , related_name="vendor")
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path , default="product.jpg")
    # description = models.TextField(null=True , blank=True  , default="I am a product")
    description =RichTextUploadingField(null=True , blank=True , default="Product")
    
    price = models.DecimalField(max_digits=7 , decimal_places=2 , default="1999")
    old_price = models.DecimalField(max_digits=7 , decimal_places=2 , default="3999")
    
    specifications = RichTextUploadingField(null=True , blank=True)
    type = models.CharField(max_length=100 , default="Organic" , null=True , blank = True)
    stock_count = models.IntegerField(default=8 , null=True , blank = True)
    life = models.CharField(max_length = 100 ,default= "6 Months", null=True , blank = True)
    
    manufacture = models.DateTimeField(auto_now_add=True , null=True , blank = True)
    tag = TaggableManager(blank=True)
    
    product_status = models.CharField(choices=STATUS , max_length=10 , default="in_review")
    
    status =  models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True , length = 4 , max_length=10 ,prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True , blank=True)
    
    class Meta:
        verbose_name_plural = "Product"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to = "product-images" , default="product.jpg")
    product = models.ForeignKey(Product ,related_name="product_images", on_delete=models.SET_NULL , null=True)
    
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
        
        

################################################## Cart , Orders , OrderTime , Address , ####################
################################################## Cart , Orders , OrderTime , Address , ####################
################################################## Cart , Orders , OrderTime , Address , ####################
################################################## Cart , Orders , OrderTime , Address , ####################
     
class CartOrder(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=7 , decimal_places=2 , default="1999")  
    paid_track = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE , max_length=30 , default="process")
    
    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder , on_delete=models.CASCADE) 
    invoice_no = models.CharField(max_length=30)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    
    price = models.DecimalField(max_digits=7 , decimal_places=2 , default="1999") 
    total = models.DecimalField(max_digits=7 , decimal_places=2 , default="1999") 
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' %(self.image))
    
    
    
    
################################################## Product Review , Whishlist , Adress ################################
################################################## Product Review , Whishlist , Adress ################################
################################################## Product Review , Whishlist , Adress ################################
################################################## Product Review , Whishlist , Adress ################################

class ProductReview(models.Model):
    
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True , related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATINGS , default=None)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating


class Whishlist(models.Model):
    
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True)

    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Whishlist"
        
    
    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    address = models.CharField(max_length=100 , null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Address"