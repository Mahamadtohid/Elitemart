from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50) 
    bio = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , null=True)
    full_name = models.CharField(max_length=200)
    name = models.CharField(max_length=100 , null = True)
    lastname = models.CharField(max_length=100 , null=True)
    bio = models.CharField(max_length=100 ,null = True , blank= True )
    profileimage = models.ImageField(upload_to = "image")
    phone = models.CharField(max_length=13)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name

class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    message = models.TextField()
    subject = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
        
    def __str__(self):
        return self.full_name