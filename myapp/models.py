from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

    def __str__(self):
        return self.product_name