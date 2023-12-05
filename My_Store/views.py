from django.http import JsonResponse
from rest_framework import status
from .models import CartItem, Product,Order ,CustomUser
from .serializers import CartItemSerializer, OrderSerializer, CustomUserSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
            "carts": "/carts/",
            "cart_detail": "/carts/<id>",
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

# ******************************************************************************


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
    
# ******************************************************************************
# ****************
# **categories**
# ****************

def get_unique_categories(request):
    if request.method == 'GET':
        categories = Product.objects.values_list('category', flat=True).distinct()
        unique_categories = list(categories)
        return JsonResponse(unique_categories, safe=False, status=status.HTTP_200_OK)

# ******************************************************************************


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

# @api_view(['GET', 'POST'])
# def carts(request):
#     if request.method == 'GET':
#         all_Orders = Order.objects.all()
#         Order_serializer = OrderSerializer(all_Orders, many=True)
#         return Response(Order_serializer.data)
    
#     elif request.method == 'POST':
#         cart_serializer = OrderSerializer(data=request.data)
#         if cart_serializer.is_valid():
#             cart_serializer.save()
#             return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ******************************************************************************

# @api_view(['GET', 'PUT', 'DELETE'])
# # @permission_classes([IsAuthenticated])
# def cart_detail(request, id):
#     try:
#         cart = Order.objects.get(pk=id, user=request.user)  # Only retrieve the cart associated with the logged-in user
#     except Order.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         cart_serializer = OrderSerializer(cart)
#         return Response(cart_serializer.data)
    
#     elif request.method == 'PUT':
#         cart_serializer = OrderSerializer(cart, data=request.data)
#         if cart_serializer.is_valid():
#             cart_serializer.save()
#             return Response(cart_serializer.data)
#         return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         cart.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ******************************************************************************

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

# ******************************************************************************

@api_view(['GET'])
def user_cart_items(request, user_id):
    try:
        cart_items = CartItem.objects.filter(user=user_id)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        return Response(cart_items_serializer.data)

# ******************************************************************************
    
def get_username_by_id(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        username = user.username
        return JsonResponse({'username': username})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    


# ******************************************************************************

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


# ******************************************************************************

@api_view(['DELETE'])
def delete_cart_item(request, user_id, product_id):
    try:
        cart_item = CartItem.objects.filter(user=user_id, product=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



    # new_order = Order()
    # new_order.save()
    # cartItems = CartItem.objects.all() # bring cart items for this user. (all cart items that order = null)
    # for item in cartItems:
    #     item.order = new_order
    #     item.save()