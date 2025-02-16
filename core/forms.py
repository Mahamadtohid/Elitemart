from django import forms 
from core.models import ProductReview

class productReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Write review'}))
    
    class Meta:
        model = ProductReview
        fields = ['review' , 'rating']