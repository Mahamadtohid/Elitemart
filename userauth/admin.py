from django.contrib import admin
from userauth.models import *

# from import_ex


class userAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'message']
    

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user','full_name', 'bio' , 'phone']

admin.site.register(User , userAdmin)
admin.site.register(ContactUs , ContactUsAdmin)
admin.site.register(Profile)
# Register your models here.
