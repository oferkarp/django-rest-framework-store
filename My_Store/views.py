from django.http import JsonResponse
from rest_framework import status
from .models import CartItem, Product,Order ,CustomUser
from .serializers import CartItemSerializer, OrderSerializer, CustomUserSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


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


# ************************
# **not use in the front**
# ************************

@api_view(['GET', 'PUT', 'DELETE'])
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

# # @permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
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

# # @permission_classes([IsAuthenticated])
@api_view(['GET'])
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

# # @permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_cart_item(request, user_id, product_id):
    try:
        cart_item = CartItem.objects.filter(user=user_id, product=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# ******************************************************************************

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def checkout_view(request):
    if request.method == 'POST':
        # Get the cart items data from the request payload
        cart_items_data = request.data.get('cartItems', [])

        # Create an order for the user
        order = Order.objects.create()

        # Iterate through cart items data and create CartItem objects associated with the order
        for item_data in cart_items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity')

            # Creating CartItem instances based on the provided data
            cart_item = CartItem.objects.create(
                user=request.user,  # Retrieve the user from the request
                product_id=product_id,
                quantity=quantity,
                order=order  # Associate the cart item with the newly created order
            )

        return Response({'message': 'Checkout successful!'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)












    # new_order = Order()
    # new_order.save()
    # cartItems = CartItem.objects.all() # bring cart items for this user. (all cart items that order = null)
    # for item in cartItems:
    #     item.order = new_order
    #     item.save()