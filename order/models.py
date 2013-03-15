#coding:utf-8
from django.db import models

# Create your models here.

class OrderInfo(models.Model):
    orderSn = models.IntegerField()
    user = models.CharField(max_length=30,blank=True,null=True)
    postscript = models.CharField(max_length=255,blank=True,null=True)
    referer = models.CharField(max_length=30)
    orderType = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s" % self.orderSn

class OrderItem(models.Model):
    orderSn = models.ForeignKey(OrderInfo)
    itemName = models.CharField(max_length=30)
    attrValue = models.CharField(max_length=30)
    number = models.SmallIntegerField()
    itemType = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s - %s [%s][n:%s][t:%s]" % ( self.orderSn, self.itemName, self.attrValue, self.number, self.itemType )

class OrderFee(models.Model):
    orderSn = models.ForeignKey(OrderInfo)
    itemName = models.ForeignKey(OrderItem)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u"%s - %s" % ( self.orderSn, self.amount )