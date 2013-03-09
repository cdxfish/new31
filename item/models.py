#coding:utf-8
from django.db import models
from shop.models import *

# Create your models here.

class Item(models.Model):
    itemName = models.CharField(max_length=30)
    sn = models.CharField(max_length=30)
    addTime = models.DateTimeField()
    shelf = models.BooleanField()
    show = models.BooleanField()
    desc = models.CharField(max_length=60)
    keywords = models.CharField(max_length=30)
    like = models.IntegerField()
    click = models.IntegerField()

    def __unicode__(self):
        return u"%s - %s [ shelf: %s ] [ show: %s ]" % (self.itemName, self.sn, self.shelf, self.show)

class ItemAttr(models.Model):
    itemName = models.ForeignKey(Item)
    attrValue = models.ForeignKey(AttriBute)

    def __unicode__(self):
        return u"%s - %s" % (self.itemName, self.attrValue)

    class Meta:
        ordering = ['attrValue']

class ItemDiscount(models.Model):
    itemAttr = models.ForeignKey(ItemAttr)
    discount = models.ForeignKey(Discount)

    def __unicode__(self):
        return u"%s - %s" % (self.itemAttr, self.discount)

class ItemFee(models.Model):
    itemAttr = models.ForeignKey(ItemAttr)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    itemType = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s - %s" % (self.itemAttr, self.amount)

    class Meta:
        ordering = ['amount']        