from django.db import models
from passlib.hash import pbkdf2_sha256
import datetime
import os


# Source:
# https://www.dangtrinh.com/2015/11/django-imagefield-rename-file-on-upload.html
# Accessed on March 9 2019
def path_and_rename(instance, filename):
    upload_to = 'media'
    ext = filename.split('.')[-1]
    # get filename
    filename = '{}.{}'.format(instance.name, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Order(models.Model):
    cardID = models.IntegerField()
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class Seller(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    description = models.CharField(max_length=100)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.password = pbkdf2_sha256.hash(self.password, rounds=1200, salt_size=32)
        super().save(force_insert, force_update, using, update_fields)


class Menu(models.Model):
    image = models.ImageField(upload_to=path_and_rename)
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
