from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import pre_save,post_save

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.BooleanField(default=False)
    total_price  = models.FloatField(default=0)


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    total_items = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
# Create your models here.
