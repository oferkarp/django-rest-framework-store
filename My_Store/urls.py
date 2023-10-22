from django.urls import path

from My_Store import views


urlpatterns = [
    path('products/', views.products, name='all_products'),
    path('products/<id>', views.product_detail, name="product_detail"),
    path('carts/', views.carts, name='all_products'),
    path('carts/<id>', views.cart_detail, name="product_detail"),
    path('cart_items/', views.cart_items, name='all_products'),
    path('cart_items/<id>', views.cart_item_detail, name="product_detail"),
]