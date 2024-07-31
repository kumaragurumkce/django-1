from django.contrib import admin
from .models import Image, CategoryType, SubCategory, Product

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'collection_category', 'uploaded_at')
    list_filter = ('category', 'collection_category')
    search_fields = ('title',)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'subcategory', 'price')
    list_filter = ('subcategory',)
    search_fields = ('product_name', 'description')

admin.site.register(Image, ImageAdmin)
admin.site.register(CategoryType)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
