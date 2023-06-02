from itertools import product
from urllib import response
from django.shortcuts import render, get_object_or_404
from api.filters import ProductFilter
from rest_framework.decorators import api_view
from .serializers import *
from storeapp.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser



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
8
        
            

class CartViewSet(CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    
    http_method_names = ["get", "post", "patch", "delete"]
    
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}



class OrderViewSet(ModelViewSet):
    
    http_method_names = ["get", "patch", "post", "delete", "options", "head"]
    
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
            
    
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={"user_id": self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
    

    
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
       
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)
    
    # def get_serializer_context(self):
    #     return {"user_id": self.request.user.id}
            
        



class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        bio = request.data["bio"]
        picture = request.data["picture"]
        
        Profile.objects.create(name = name, bio = bio, picture=picture)
        
        
        return Response("Profile created successfully", status=status.HTTP_200_OK)