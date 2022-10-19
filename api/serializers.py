from itertools import product
from rest_framework import serializers
from  storeapp.models import Cart, Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [ "id", "name", "description", "category", "slug", "inventory", "price"]
    
    category = CategorySerializer()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date_created", "name", "description"]
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id = product_id,  **validated_data)

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Cart
        fields = ["id"]

