from django.db import models
from passlib.hash import pbkdf2_sha256
import datetime



class Order(models.Model):
    cardID = models.IntegerField()
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class Seller(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=256)
    description = models.CharField(max_length=100)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.password = pbkdf2_sha256.hash(self.password, rounds=1200, salt_size=32)
        super().save(force_insert, force_update, using, update_fields)


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
    # orderTime = models.DateTimeField(auto_now_add=True)
    # finishTime = models.DateTimeField(auto_now=True)
    finishTime = models.DateTimeField(null=True, blank=True)
    sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.done:
            self.finishTime = datetime.datetime.now()
        super().save(force_insert, force_update, using, update_fields)



# class QueueTransaction(models.Model):
#     orderID = models.ForeignKey(Order, on_delete=models.PROTECT)
#     menuID = models.ForeignKey(Menu, on_delete=models.PROTECT)
#     price = models.IntegerField()
#     qty = models.IntegerField()
#     tableNumber = models.IntegerField()
#     sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)
#     orderTime = models.DateTimeField(auto_now_add=True)