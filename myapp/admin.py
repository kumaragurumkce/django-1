from django.contrib import admin
from .models import Image, CategoryType, SubCategory, Product, Contact,Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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
    



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['user_type']  # Ensure 'user_type' is editable in admin

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Image, ImageAdmin)
admin.site.register(CategoryType,CategoryTypeAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact,ContactAdmin)