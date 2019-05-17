from rest_framework import serializers

from webserver.models import Menu
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
        fields = ('id', 'image', 'name', 'price', 'category', 'availability', 'sellerID', 'qty')


class OrderDetailSerializer(serializers.ModelSerializer):
    orderTime = serializers.DateTimeField(source='orderID.time', read_only=True)
    menuName = serializers.CharField(source='menuID.name', read_only=True)
    image = serializers.ImageField(source='menuID.image', read_only=True)
    # sellerID = serializers.CharField(source='menuID.sellerID.id', read_only=True)
    class Meta:
        model = models.OrderDetail
        fields = ('id', 'orderID', 'sellerID', 'menuID', 'menuName', 'image', 'price', 'qty',
                  'tableNumber', 'done', 'orderTime', 'finishTime')

    def validate(self, data):
        # print(self)
        # print(data)
        menuID = data['menuID'].id
        print(type(data['qty']))
        print("data['qty']: ".format(int(data['qty'])))
        print("Menu ID: {}".format(menuID))
        menuObject = Menu.objects.get(id=menuID)
        print("menuObject.qty: {}".format(menuObject.qty))
        tempQty = int(menuObject.qty) - (data['qty'])
        print("tempQty= {}".format(tempQty))
        if tempQty < 0:
            raise serializers.ValidationError("{}".format(menuObject.name))
        return data



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
