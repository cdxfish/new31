from django.db import models
# from django.contrib.sites.models import *

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

class AttriBute(models.Model):
    attr = models.CharField(max_length=30)

class Discount(models.Model):
    discount = models.CharField(max_length=30)

class Tag(models.Model):
    tag = models.CharField(max_length=30)

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

class ItemTag(models.Model):
    tag = models.ManyToManyField(Tag)
    name = models.ManyToManyField(Item)



