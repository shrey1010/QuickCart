from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import razorpay
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


class CreateOrderView(APIView):
    def post(self, request):
        try:
            razorpay_client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount = request.data['amount']
            order = razorpay_client.order.create({
                'amount': amount * 100,
                'currency': 'INR',
                'payment_capture': 1
            })
            serializer = OrderSerializer(data={
                'user': request.user.id,
                'amount': amount,
                'razorpay_order_id': order['id']
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(order, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

class PaymentCallbackView(APIView):
    def post(self, request):
        try:
            razorpay_client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_payment_id = request.data['razorpay_payment_id']
            razorpay_order_id = request.data['razorpay_order_id']
            signature = request.data['razorpay_signature']
            params_dict = {
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': signature
            }
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                order.status = 'COMPLETED'
                order.save()
                cart = Cart.objects.filter(user=request.user)
                cart.delete()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            except:
                return Response({'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
