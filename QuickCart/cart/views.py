from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from products.models import Product
# Create your views here.

class CartView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args,**kwargs):
        user = request.user
        cart = Cart.objects.filter(user = user ,ordered= False).first()
        queryset = CartItems.objects.filter(cart = cart)
        serialzier = CartItemSerializer(queryset,many = True)
        return Response(serialzier.data)
        
    def post(self, request, *args,**kwargs):
        user = request.user
        data = request.data
        cart,_ = Cart.objects.get_or_create(user = user , ordered= False)
        product  = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = cart_items(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()
        cart_items = CartItems.objects.filter(user = user , cart = cart.id)
        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({"success":"Items added to cart successfully"})

    def put(self, request, *args,**kwargs):
        data = request.data
        cart_item = CartItems.objects.get(id = data.get("id"))
        quantity = data.get("quantity")
        cart_item += quantity
        cart_item.save()
        return Response({"success": "Items updated  in cart successfully"})

    def delete(self, request, *args,**kwargs):
        user = request.user
        data = request.data
        cart_item = CartItems.objects.get(id = data.get("id"))
        cart_item.delete()
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serialzier = CartItemSerializer(queryset, many=True)
        return Response(serialzier.data)
    
class OrderAPI(APIView):
    def get(self, request):
        query_set = Order.objects.filter(user = request.user)
        serailizers = OrderSerializer(query_set, many=True)
        return Response(serailizers.data)
