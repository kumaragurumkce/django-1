from django import forms
from .models import Image,User,Product,Contact
from django.contrib.auth.forms import UserCreationForm

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'category', 'collection_category', 'image','uploaded_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection_category'].required = False


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerUserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    username = forms.CharField(
        max_length=20,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    password1 = forms.CharField(
        max_length=24,
        required=True,
        help_text='Required.',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        required=True,
        help_text='Required.',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields= ['product_name','image','subcategory','price','description']
        
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','feedback']