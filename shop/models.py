#coding:utf-8

from django.db import models

# Create your models here.
class AttriBute(models.Model):
    attrValue = models.CharField(u'规格', max_length=30, unique=True)

    def __unicode__(self):
        return u"%s" % self.attrValue

class Discount(models.Model):
    discount = models.DecimalField(u'折扣', max_digits=3, decimal_places=1)

    def __unicode__(self):
        return u"%s" % self.discount

class Ad(models.Model):
    url = models.CharField(u'链接地址', max_length=60)
    img = models.CharField(u'图片地址', max_length=60)
    show = models.BooleanField(u'是否显示', default=False)
    vieworder = models.SmallIntegerField(u'排序')

    def __unicode__(self):
        return u"%s" % self.img

class Logistics(models.Model):
    value = models.CharField(u'物流时间', max_length=60, unique=True)
    isOpen = models.BooleanField(u'是否可选', max_length=60)
    vieworder = models.SmallIntegerField(u'排序')

    def __unicode__(self):
        return u"%s" % self.value

class SignTime(models.Model):
    value = models.CharField(u'收货时间', max_length=60, unique=True)
    isOpen = models.BooleanField(u'是否可选', max_length=60)
    vieworder = models.SmallIntegerField(u'排序')

    def __unicode__(self):
        return u"%s" % self.value
        
class Image(models.Model):
    value = models.ImageField(u'图片', upload_to='/upload')

    def __unicode__(self):
        return u"%s" % self.value