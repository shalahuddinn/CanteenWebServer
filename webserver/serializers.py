from rest_framework import serializers
from . import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ('id', 'cardID', 'amount', 'time')


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seller
        fields = ('id', 'username', 'password')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = ('id', 'image', 'name', 'price', 'category', 'availability', 'sellerID')


class OrderDetailSerializer(serializers.ModelSerializer):
    orderTime = serializers.DateTimeField(source='orderID.time', read_only=True)
    menuName = serializers.CharField(source='menuID.name', read_only=True)
    image = serializers.ImageField(source='menuID.image', read_only=True)
    # sellerID = serializers.CharField(source='menuID.sellerID.id', read_only=True)
    class Meta:
        model = models.OrderDetail
        fields = ('id', 'orderID', 'sellerID', 'menuID', 'menuName', 'image', 'price', 'qty',
                  'tableNumber', 'done', 'orderTime', 'finishTime')

# class OrderedMenuSerializer(serializers.Serializer):
    # menuName = serializers.SlugRelatedField(many=True, read_only=True, slug_field='menuName')
    # class Meta:
    #     model = models.OrderDetail
    #     fields = ('id', 'orderID', 'menuID', 'price', 'qty', 'tableNumber', 'done', 'orderTime', 'finishTime', 'sellerID', 'menuName')
    # menu = MenuSerializer(many=True)
    # order = OrderDetailSerializer(many=True)

# class QueueTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.QueueTransaction
#         fields = ('orderID', 'menuID', 'price', 'qty', 'tableNumber', 'sellerID', 'orderTime')
