from django.db import models


class Order(models.Model):
    cardID = models.IntegerField()


class Seller(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Menu(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.IntegerField()
    availability = models.BooleanField(default=False)
    # booked = models.IntegerField()
    sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)


class OrderDetail(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.PROTECT)
    menuID = models.ForeignKey(Menu, on_delete=models.PROTECT)
    price = models.IntegerField()
    qty = models.IntegerField()
    tableNumber = models.IntegerField()
    done = models.BooleanField(default=False)
    orderTime = models.DateTimeField(auto_now_add=True)
    finishTime = models.DateTimeField(auto_now=True)
    sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)



# class QueueTransaction(models.Model):
#     orderID = models.ForeignKey(Order, on_delete=models.PROTECT)
#     menuID = models.ForeignKey(Menu, on_delete=models.PROTECT)
#     price = models.IntegerField()
#     qty = models.IntegerField()
#     tableNumber = models.IntegerField()
#     sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)
#     orderTime = models.DateTimeField(auto_now_add=True)