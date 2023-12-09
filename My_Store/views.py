from django.http import JsonResponse
from rest_framework import status
from .models import CartItem, Product,Order ,CustomUser
from .serializers import CartItemSerializer, OrderSerializer, CustomUserSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


# ****************
# **welcome_page**
# ****************

@api_view(['GET'])
def welcome_page(request):
    api_endpoints = {
        "message": "Welcome to My Store API!",
        "endpoints": {
            "all_products": "/products/",
            "product_detail": "/products/<id>",
            "unique_categories": "/products/category/",
            "cart_items": "/cart_items/",
            "user_cart_items": "user_cart_items/<int:user_id>",
            "token": "/token/",
            "token_refresh": "/token/refresh/",
            "user_name":"/user/<id>/",
            "user-registration":"/register/",
            "checkout": "/checkout/", 
            "orders": "/orders/"     
        },
        "additional_info": "Replace <id> with the respective ID in the URL."
    }
    return Response(api_endpoints)

# **************************
# **get products to navbar**
# **************************

@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        maxprice = request.GET.get('maxprice')
        category = request.GET.get('category')

        all_products = Product.objects.all()

        # Search for products based on query parameters
        if search:
            all_products = all_products.filter(name__icontains=search)
        if maxprice:
            all_products = all_products.filter(price__lte=maxprice)
        if category:
            # Ensure the category name is case-insensitive by using '__iexact'
            all_products = all_products.filter(category__iexact=category)

        # Serialize the products and return as JSON response
        all_products_json = ProductSerializer(all_products, many=True).data
        return Response(all_products_json)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ******************
# **get categories**
# ******************

def get_unique_categories(request):
    if request.method == 'GET':
        categories = Product.objects.values_list('category', flat=True).distinct()
        unique_categories = list(categories)
        return JsonResponse(unique_categories, safe=False, status=status.HTTP_200_OK)


# *************************
# **action on product get**
# *************************

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ******************************************************************************

@api_view(['GET', 'POST'])
def orders(request):
    if request.method == 'GET':
        all_Orders = Order.objects.all()
        Order_serializer = OrderSerializer(all_Orders, many=True)
        return Response(Order_serializer.data)
    
    elif request.method == 'POST':
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ***************************
# **show all the cart items**
# ***************************

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        all_cart_items = CartItem.objects.all()
        cart_item_serializer = CartItemSerializer(all_cart_items, many=True)
        return Response(cart_item_serializer.data)
    
    elif request.method == 'POST':
        cart_item_serializer = CartItemSerializer(data=request.data)
        if cart_item_serializer.is_valid():
            cart_item_serializer.save()
            return Response(cart_item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ******************************************************
# **show all the cart items per user and order is null**
# ******************************************************

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_cart_items(request, user_id):
    try:
        cart_items = CartItem.objects.filter(user=user_id, order__isnull=True)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        return Response(cart_items_serializer.data)


# **********************************
# **get id and return name of user**
# **********************************

def get_username_by_id(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        username = user.username
        return JsonResponse({'username': username})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    


# **********************************************
# **register user - get data and register user**
# **********************************************

@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)


# **************************************
# **delte product in cart item of user**
# **************************************

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, user_id, product_id):
    try:
        cart_item = CartItem.objects.filter(user=user_id, product=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# *************************
# **checkout of cart item**
# *************************

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def checkout_view(request):
    if request.method == 'POST':
        cart_items_data = request.data.get('cartItems', [])
        user_id = request.data.get('userId')  # Get the user ID from the request payload

        # Ensure the user_id is valid and exists
        if not CustomUser.objects.filter(id=user_id).exists():
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user_id=user_id)  # Create an order for the user

        for item_data in cart_items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity')

            cart_item = CartItem.objects.create(
                user_id=user_id,  # Link the cart item to the provided user ID
                product_id=product_id,
                quantity=quantity,
                order=order
            )

        return Response({'message': 'Checkout successful!'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

# *****************************************
# **delte the cart items on specific user**
# *****************************************

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def clear_cart(request, user_id):
    if request.method == 'POST':
        CustomUser = get_user_model()  # Fetch your CustomUser model

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        CartItem.objects.filter(user=user, order__isnull=True).delete()

        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# ******************
# **orders by user**
# ******************

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def user_orders(request, user_id):
    try:
        orders = Order.objects.filter(cartitem__user=user_id, cartitem__order__isnull=False).distinct()
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        orders_data = []
        for order in orders:
            order_data = {
                'id': order.id,
                'create_date': order.create_date,
                'user_id': order.user.id,
                'cart_items': []  # Placeholder for cart items
            }
            cart_items = CartItem.objects.filter(order=order)
            for cart_item in cart_items:
                cart_item_info = {
                    'product': cart_item.product.id,
                    'quantity': cart_item.quantity,
                    # Add other cart item details as needed
                }
                order_data['cart_items'].append(cart_item_info)
            orders_data.append(order_data)

        return Response(orders_data)
    
    return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
