from django.db import models
import uuid
from django.contrib.auth.models import User
# from  django.conf import settings
# from UserProfile.models import Customer

# Create your models here.

        
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default= None)
    featured_product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='featured_product')
    icon = models.CharField(max_length=100, default=None, blank = True, null=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name = "reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description

    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models. BooleanField(default=False)
    image = models.ImageField(upload_to = 'img',  blank = True, null=True, default='')
    price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    slug = models.SlugField(default=None)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.id)

class Cartitems(models.Model):
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.IntegerField(default=0)
    
 

# class SavedItem(models.Model):
#     owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
#     added = models.IntegerField(default=0)
    
    
    
#     def __str__(self):
#         return str(self.id)
    
