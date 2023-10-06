from django.urls import path

from My_Store import views


urlpatterns = [
    path('', views.products, name='all_products'),
]