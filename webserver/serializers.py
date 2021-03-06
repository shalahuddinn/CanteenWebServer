from rest_framework import serializers
from . import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ('id', 'paymentID', 'amount', 'orderTime', 'modifiedTime', 'orderStatus')


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seller
        fields = ('id', 'username', 'password')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = ('id', 'image', 'name', 'price', 'category', 'availability', 'qtyAvailable', 'qtyOnBooked', 'sellerID')


class OrderDetailSerializer(serializers.ModelSerializer):
    orderTime = serializers.DateTimeField(source='orderID.orderTime', read_only=True)
    orderStatus = serializers.CharField(source='orderID.orderStatus', read_only=True)
    menuName = serializers.CharField(source='menuID.name', read_only=True)
    image = serializers.ImageField(source='menuID.image', read_only=True)
    cardID = serializers.SerializerMethodField('getCardID')

    def getCardID(self, instance):
        paymentID = instance.orderID.paymentID
        if paymentID != 0:
        # print("Payment ID:{}".format(paymentID))
            paymentObject = models.Payment.objects.get(id=paymentID)
            cardID = paymentObject.cardID
        else:
            cardID = "null"
        return cardID

    class Meta:
        model = models.OrderDetail
        # fields = ('id', 'orderID', 'sellerID', 'menuID', 'menuName', 'image', 'price', 'qty',
        #           'tableNumber', 'done', 'orderTime', 'finishTime', 'orderStatus')
        fields = ('id', 'orderID', 'cardID', 'sellerID', 'menuID', 'menuName', 'image', 'price', 'qty',
                  'tableNumber', 'orderTime', 'modifiedTime', 'orderStatus', 'itemStatus')

    def validate(self, data):
        if self.context.get("request").method == "POST":
            # if self.data.req.method =="POST":
            # print(self)
            # print(data)
            menuID = data['menuID'].id
            # print(type(data['qty']))
            # print("data['qty']: ".format(int(data['qty'])))
            # print("Menu ID: {}".format(menuID))
            menuObject = models.Menu.objects.get(id=menuID)
            if not menuObject.availability:
                raise serializers.ValidationError("Tidak Tersedia: {}".format(menuObject.name))
                # print("tempQty= {}".format(tempQty))
            tempQty = int(menuObject.qtyAvailable) - (data['qty'])
            if tempQty < 0:
                raise serializers.ValidationError("Stok Tidak Cukup: {}".format(menuObject.name))
            # print("menuObject.qty: {}".format(menuObject.qty))
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = ('id', 'cardID', 'amount', 'time', 'orderID')



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
