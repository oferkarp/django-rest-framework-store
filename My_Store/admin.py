from django.contrib import admin
from .models import Product,Order,CartItem,CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'age', 'city')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'age', 'city'),
        }),
    )

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)