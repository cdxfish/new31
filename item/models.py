from django.db import models
from shop.models import *

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=30)
    sn = models.CharField(max_length=30)
    add_time = models.DateTimeField()
    shelf = models.BooleanField()
    show = models.BooleanField()
    desc = models.CharField(max_length=60)
    keywords = models.CharField(max_length=30)
    like = models.IntegerField()
    click = models.CharField(max_length=30)

class ItemAttr(models.Model):
    name = models.ManyToManyField(Item)
    attr = models.ManyToManyField(AttriBute)

class ItemDiscount(models.Model):
    name = models.ManyToManyField(Item)
    discount = models.ManyToManyField(Discount)

class ItemFee(models.Model):
    name = models.ManyToManyField(Item)
    amount = models.ManyToManyField(Discount)
    type = models.FloatField()


