from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from userauth.models import User , Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    

    class Meta:
        model = User
        fields = ['username' , 'email']
        
        
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    # email = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Email Address"}))
    # profileimage = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Profile image"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"phone"}))
    
    class Meta:
        model = Profile
        fields = ['full_name' , 'profileimage' , 'bio' , 'phone']
    