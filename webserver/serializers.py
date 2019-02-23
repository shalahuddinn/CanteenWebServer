from rest_framework import serializers
from . import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ('id', 'cardID')


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seller
        fields = ('id', 'username', 'password')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = ('id', 'image', 'name', 'price', 'category', 'availability', 'sellerID')


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields = ('id', 'orderID', 'menuID', 'price', 'qty', 'tableNumber', 'done', 'orderTime', 'finishTime', 'sellerID')

# class QueueTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.QueueTransaction
#         fields = ('orderID', 'menuID', 'price', 'qty', 'tableNumber', 'sellerID', 'orderTime')