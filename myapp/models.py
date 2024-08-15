from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin

class Category(models.TextChoices):
    HOME = 'home', 'Home'
    COLLECTIONS = 'collections', 'Collections'
    TRENDS = 'trends', 'Trends'
    
class CollectionCategory(models.TextChoices):
    SAREE = 'saree', 'Saree'
    PANT = 'pant', 'Pant'

class Image(models.Model):
    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    collection_category = models.CharField(max_length=20, choices=CollectionCategory.choices, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class CategoryType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_product/')
    
    

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    out_of_stock = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.out_of_stock = self.quantity == 0
        super().save(*args, **kwargs)
    
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=40)
    feedback=models.CharField(max_length=250)
    
class Profile(models.Model):
    ADMIN = 0
    CUSTOMER = 1
    
    USER_TYPE_CHOICES = [
        (ADMIN,'Admin'),
        (CUSTOMER,'Customer'),
    ]
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type=models.IntegerField(choices=USER_TYPE_CHOICES,default=CUSTOMER)
    

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    

@admin.register(Profile)
class Admin(admin.ModelAdmin):
    list_display=('user','user_type')
