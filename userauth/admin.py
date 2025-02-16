from django.contrib import admin
from userauth.models import User

# from import_ex


class userAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')

admin.site.register(User , userAdmin)
# Register your models here.
