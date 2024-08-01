# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='home_content'),
    path('home/',views.home_content,name='home_content'),
    path('collections/', views.collections_page, name='collections_content'),
    path('trends/', views.trends_page, name='trends_content'),
    path('about/', views.about_page, name='about_content'),
    path('contact/', views.contact_page, name='contact_content'),
    path('addCart/<int:pk>/', views.addCart_page, name='addCart_content'),
    path('updateCart/<int:pk>/', views.updateCart_page, name='updateCart_content'),
    path('deleteCart/<int:pk>/', views.deleteCart_page, name='deleteCart_content'),
    path('deleteCartItem/<int:pk>/', views.deleteCartItem, name='deleteCart_Item'),
    
    path('cartlist/', views.cartList_page, name='cartList_content'),
    path('upload/', views.image_upload, name='image_upload'),
    path('UploadList/', views.image_list, name='image_list'),
    path('UploadList/<str:category>/', views.image_list, name='image_list'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('product_create/', views.product_create, name='product_create'),
    path('product_list', views.product_list, name='product_list'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),



    
    
    
    

]