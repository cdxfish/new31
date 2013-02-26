#coding:utf-8
from django.db import models
from shop.models import *

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=30)
    sn = models.CharField(max_length=30)
    addTime = models.DateTimeField()
    shelf = models.BooleanField()
    show = models.BooleanField()
    desc = models.CharField(max_length=60)
    keywords = models.CharField(max_length=30)
    like = models.IntegerField()
    click = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s - %s [ shelf: %s ] [ show: %s ]" % (self.name, self.sn, self.shelf, self.show)

class ItemAttr(models.Model):
    name = models.ForeignKey(Item)
    value = models.ForeignKey(AttriBute)

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.value)

class ItemDiscount(models.Model):
    itemAttr = models.ForeignKey(ItemAttr)
    discount = models.ForeignKey(Discount)

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.discount)

class ItemFee(models.Model):
    itemAttr = models.ForeignKey(ItemAttr)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.amount)