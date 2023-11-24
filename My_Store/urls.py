from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from My_Store import views


urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('products/', views.products, name='all_products'),
    path('products/<id>', views.product_detail, name="product_detail"),
    path('products/category/', views.get_unique_categories, name='unique_categories'),
    path('carts/', views.carts, name='carts'),
    path('carts/<id>', views.cart_detail, name="cart_detail"),
    path('cart_items/', views.cart_items, name='cart_items'),
    path('cart_items/<id>', views.cart_item_detail, name="cart_item_detail"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]