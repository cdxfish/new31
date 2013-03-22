#coding:utf-8
from django.db import models
from shop.models import *
from tag.models import *

# Create your models here.

class itemManager(models.Manager):
    def getItemByItemName(self, itemName = ''):

        return self.select_related().get(itemName=itemName)

    def getTagByItemName(self, itemName = ''):

        return self.select_related().get(itemName=itemName).tag.all()


class itemDescManager(models.Manager):
    def random(self, itemName = ''):

        return self.select_related().all()[0]


class Item(models.Model):
    itemName = models.CharField(u'商品名称', max_length=30, unique=True)
    sn = models.IntegerField(u'货号', unique=True)
    addTime = models.DateTimeField(u'添加时间', auto_now=True, auto_now_add=True)
    onLine = models.BooleanField(u'上架', default=False)
    show = models.BooleanField(u'商城可见', default=False)
    like = models.IntegerField(u'喜欢', default=0, editable=False)
    click = models.IntegerField(u'点击', default=0, editable=False)
    tag = models.ManyToManyField(Tag, verbose_name=u'标签')

    objects = itemManager()

    def __unicode__(self):
        return u"%s - %s [ onLine: %s ] [ show: %s ]" % (self.itemName, self.sn, self.onLine, self.show)


class ItemDesc(models.Model):
    itemName = models.ForeignKey(Item, verbose_name=u'商品')
    desc = models.CharField(u'描述', max_length=60)
    objects = itemDescManager()

    def __unicode__(self):
        return u"%s - %s" % (self.itemName, self.desc)

    class Meta:
        ordering = ['?']
        unique_together=(("itemName","desc"),)     


class ItemAttr(models.Model):
    itemName = models.ForeignKey(Item, verbose_name=u'商品')
    attrValue = models.ForeignKey(AttriBute, verbose_name=u'规格')

    def __unicode__(self):
        return u"%s - %s" % (self.itemName, self.attrValue)

    class Meta:
        ordering = ['attrValue']
        unique_together=(("itemName","attrValue"),)           


class ItemFee(models.Model):
    itemAttr = models.ForeignKey(ItemAttr, verbose_name=u'规格', unique=True)
    amount = models.DecimalField(u'单价', max_digits=10, decimal_places=2)
    itemType = models.SmallIntegerField(u'类型')

    def __unicode__(self):
        return u"%s - %s" % (self.itemAttr, self.amount)

    class Meta:
        ordering = ['amount']


class ItemDiscount(models.Model):
    itemFee = models.ForeignKey(ItemFee, verbose_name=u'单价', unique=True)
    discount = models.ForeignKey(Discount, verbose_name=u'折扣')

    def __unicode__(self):
        return u"%s - %s" % (self.itemFee, self.discount)


class ItemImg(models.Model):
    itemName = models.ForeignKey(Item, verbose_name=u'商品')
    img = models.ImageField(u'图片', upload_to='images')

    def __unicode__(self):
        return u"%s - %s" % (self.itemName, self.img)

    class Meta:
        ordering = ['?']
