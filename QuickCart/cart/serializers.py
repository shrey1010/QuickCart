from rest_framework import serializers
from .models import *
from products.serializers import *


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = CartSerializer()
    class Meta:
        model = CartItems
        fields = "__all__"


