from django import forms
from .models import Image,User,Product,Contact,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'category', 'collection_category', 'image','uploaded_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection_category'].required = False


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields= ['product_name','image','subcategory','price','description','quantity']
        
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','feedback']
        
class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','email','password']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []
        
class UserLoginForm(AuthenticationForm):
    pass