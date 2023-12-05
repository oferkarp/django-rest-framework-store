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
    path('user_cart_items/<int:user_id>', views.user_cart_items, name='user_cart_items'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:user_id>/', views.get_username_by_id, name='get_username_by_id'),
    path('register/', views.user_registration, name='user-registration'),
    path('user_cart_items/delete/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),

]