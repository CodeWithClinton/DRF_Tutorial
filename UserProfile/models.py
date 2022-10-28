from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # username = models.CharField(max_length=100, default= None, null=True, blank=True)
    first_name = models.CharField(max_length=100, default= None, null=True, blank=True)
    last_name = models.CharField(max_length=100, default= None, null=True, blank=True)
    email = models.EmailField(max_length=100, default= None, null=True, blank=True, unique=True)
    
    
    def __str__(self):
        return self.first_name

class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, default='')
    home_address = models.CharField(max_length=50)
    bus_stop = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    
    def __str__(self):
        return self.home_address

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def CreateCustomer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        customer.first_name = instance.first_name
        customer.last_name = instance.last_name
        customer.email = instance.email
        customer.save()


@receiver(post_save, sender=Customer)
def createProfile(sender, instance, created, *args, **kwargs):
    customer_user = instance.user
    if created == False:
        customer_user.first_name= instance.first_name
        customer_user.email = instance.email
        customer_user.last_name = instance.last_name
        customer_user.save()

        
    

    