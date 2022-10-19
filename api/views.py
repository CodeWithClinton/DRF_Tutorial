from itertools import product
from urllib import response
from django.shortcuts import render, get_object_or_404
from api.filters import ProductFilter
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from storeapp.models import Category, Product, Review
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination



from api import serializers

# Create your views here.
class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['old_price']
    pagination_class = PageNumberPagination



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
         return Review.objects.filter(product_id=self.kwargs["product_pk"])
    
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}

        
            
        

