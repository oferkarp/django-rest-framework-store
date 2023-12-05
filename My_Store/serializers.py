from rest_framework import serializers
from .models import Product, Order, CartItem, CustomUser

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    Order_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'age', 'city']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
