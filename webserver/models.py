from django.db import models
from django.http import JsonResponse
from rest_framework import serializers
from django.utils import timezone
from passlib.hash import pbkdf2_sha256

import datetime
import os


# Source:
# https://www.dangtrinh.com/2015/11/django-imagefield-rename-file-on-upload.html
# Accessed on March 9 2019
def path_and_rename(instance, filename):
    upload_to = 'media'
    ext = filename.split('.')[-1]
    # Get filename
    filename = '{}.{}'.format(instance.name, ext)
    # Return the whole path to the file
    return os.path.join(upload_to, filename)


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('placed', 'Placed'),
        ('paid', 'Paid'),
        ('expired', 'Expired'),
        ('cancel', 'Cancel')
    )
    paymentID = models.IntegerField(default=0)
    amount = models.IntegerField()
    orderTime = models.DateTimeField(auto_now_add=True)
    # expiredTime = models.DateTimeField(default=(timezone.now() + timezone.timedelta(minutes=1)))
    modifiedTime = models.DateTimeField(auto_now=True)
    orderStatus = models.CharField(default="placed", null=False, max_length=7, choices=ORDER_STATUS_CHOICES)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.orderStatus == "expired" or self.orderStatus == "cancel":
            orderDetailObject = OrderDetail.objects.get(orderID=self.id)

            menuID = orderDetailObject.menuID.id
            menuObject = Menu.objects.get(id=menuID)
            tempQty = menuObject.qty + orderDetailObject.qty
            menuObject.qty = tempQty
            menuObject.save()

            # tempQty = menuObject.qty - self.qty
            # menuObject.qty = tempQty
            # menuObject.save()


        super().save(force_insert, force_update, using, update_fields)


class Seller(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    description = models.CharField(max_length=100)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.password = pbkdf2_sha256.hash(self.password, rounds=1200, salt_size=32)
        super().save(force_insert, force_update, using, update_fields)


class Menu(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('drink', 'Drink')
    )
    image = models.ImageField(upload_to=path_and_rename)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    availability = models.BooleanField(default=False)
    qty = models.IntegerField(default=100)
    # booked = models.IntegerField()
    sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)


class OrderDetail(models.Model):
    ITEM_STATUS_CHOICES = (
        ('done', 'Done'),
        ('reject', 'Reject'),
        ('placed', 'Placed')
    )
    orderID = models.ForeignKey(Order, on_delete=models.PROTECT)
    menuID = models.ForeignKey(Menu, on_delete=models.PROTECT)
    price = models.IntegerField()
    qty = models.IntegerField()
    tableNumber = models.IntegerField()
    # done = models.BooleanField(default=False)
    # orderTime = models.DateTimeField(auto_now_add=True)
    # finishTime = models.DateTimeField(auto_now=True)
    modifiedTime = models.DateTimeField(auto_now=True)
    sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)
    itemStatus = models.CharField(default="placed", null=False, max_length=6, choices=ITEM_STATUS_CHOICES)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.itemStatus == "placed":
            menuID = self.menuID.id
            menuObject = Menu.objects.get(id=menuID)
            tempQty = menuObject.qty - self.qty
            menuObject.qty = tempQty
            menuObject.save()

        # if self.done:
            # self.finishTime = datetime.datetime.now()
        # else:
        #     menuID = self.menuID.id
        #     menuObject = Menu.objects.get(id=menuID)
        #     tempQty = menuObject.qty - self.qty
        #     menuObject.qty = tempQty
        #     menuObject.save()
        super().save(force_insert, force_update, using, update_fields)


class Payment(models.Model):
    cardID = models.IntegerField()
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


# class QueueTransaction(models.Model):
#     orderID = models.ForeignKey(Order, on_delete=models.PROTECT)
#     menuID = models.ForeignKey(Menu, on_delete=models.PROTECT)
#     price = models.IntegerField()
#     qty = models.IntegerField()
#     tableNumber = models.IntegerField()
#     sellerID = models.ForeignKey(Seller, on_delete=models.PROTECT)
#     orderTime = models.DateTimeField(auto_now_add=True)
