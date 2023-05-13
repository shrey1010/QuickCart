from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ShippingOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    pincode = models.PositiveIntegerField()
    phone_number =models.PositiveIntegerField()
