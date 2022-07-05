from urllib import response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer
from storeapp.models import Category, Product
from rest_framework.response import Response
from rest_framework import status

from api import serializers

# Create your views here.

@api_view()
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

        


@api_view()
def api_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
  
        


@api_view()
def api_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view()
def api_category(request, pk):
    category = get_object_or_404(Category, category_id=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

