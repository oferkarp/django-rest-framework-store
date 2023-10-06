from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from My_Store.models import Product


from My_Store.serializers import ProductSerializer




# I want to call 127.0.0.1/Products -> and return a json of all the products
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)
