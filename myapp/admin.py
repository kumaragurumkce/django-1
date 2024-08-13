from django.contrib import admin
from .models import Image, CategoryType, SubCategory, Product, Contact

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'collection_category', 'uploaded_at')
    list_filter = ('category', 'collection_category')
    search_fields = ('title',)
class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)
    list_filter = ('name',)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'subcategory', 'price')
    list_filter = ('subcategory',)
    search_fields = ('product_name', 'description')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','feedback')
admin.site.register(Image, ImageAdmin)
admin.site.register(CategoryType,CategoryTypeAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact,ContactAdmin)