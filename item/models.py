#coding:utf-8

from django.db import models
from tag.models import *
from spec.models import *
from discount.models import *

# Create your models here.

class itemManager(models.Manager):
    def getItemByItemName(self, itemName = ''):

        return self.select_related().get(name=itemName)

    def getTagByItemName(self, itemName = ''):

        return self.select_related().get(name=itemName).tag.all()

    def getItemByItemSpecId(self, id = ''):

        item = ItemSpec.objects.select_related().get(id=id,onLine=True,show=True).item

        if item.onLine and item.show:

            return item
        else:
            raise self.DoesNotExist


class itemDescManager(models.Manager):
    def random(self, itemName = ''):

        return self.select_related().all()[0]


class itemSpecManager(models.Manager):
    def getSpecByItemId(self, id = ''):

        return Item.objects.select_related().get(id=id, onLine=True, show=True).itemspec_set.all()

    def getSpecByItemSpecId(self, id = ''):

        itemSpec = ItemSpec.objects.select_related().get(id=id)

        if itemSpec.item.onLine and itemSpec.item.show:

            return itemSpec
        else:
            raise self.DoesNotExist


class Item(models.Model):
    name = models.CharField(u'商品名称', max_length=30, unique=True)
    sn = models.IntegerField(u'货号', unique=True)
    addTime = models.DateTimeField(u'添加时间', auto_now=True, auto_now_add=True)
    onLine = models.BooleanField(u'上架', default=False)
    show = models.BooleanField(u'商城可见', default=False)
    like = models.IntegerField(u'喜欢', default=0, editable=False)
    click = models.IntegerField(u'点击', default=0, editable=False)
    tag = models.ManyToManyField(Tag, verbose_name=u'标签')

    objects = itemManager()

    def __unicode__(self):
        return u"%s - %s [ onLine: %s ] [ show: %s ]" % (self.name, self.sn, self.onLine, self.show)


class ItemDesc(models.Model):
    item = models.ForeignKey(Item, verbose_name=u'商品')
    desc = models.CharField(u'描述', max_length=60)
    objects = itemDescManager()

    def __unicode__(self):
        return u"%s - %s" % (self.item, self.desc)

    class Meta:
        ordering = ['?']
        unique_together=(("item","desc"),)     


class ItemSpec(models.Model):
    item = models.ForeignKey(Item, verbose_name=u'商品')
    spec = models.ForeignKey(Spec, verbose_name=u'规格')
    onLine = models.BooleanField(u'上线', default=False)
    show = models.BooleanField(u'商城可见', default=False)
    objects = itemSpecManager()

    def __unicode__(self):
        return u"%s - %s [ onLine: %s ][ show: %s ]" % (self.item, self.spec, self.onLine, self.show)

    class Meta:
        ordering = ['spec']
        unique_together=(("item","spec"),)           


class ItemFee(models.Model):
    itemSpec = models.ForeignKey(ItemSpec, verbose_name=u'规格', unique=True)
    amount = models.DecimalField(u'单价', max_digits=10, decimal_places=2)
    itemType = models.SmallIntegerField(u'类型',choices=((1,u'零售价'),(2,u'积分换购价'),))

    def __unicode__(self):
        return u"%s - %s [%s]" % (self.itemSpec, self.amount, self.get_itemType_display())

    class Meta:
        ordering = ['amount']
        unique_together=(("itemSpec","amount","itemType"),)   


class ItemDiscount(models.Model):
    itemFee = models.ForeignKey(ItemFee, verbose_name=u'单价', unique=True)
    discount = models.ForeignKey(Discount, verbose_name=u'折扣')

    def __unicode__(self):
        return u"%s - %s 折" % (self.itemFee, self.discount)


class ItemImg(models.Model):
    item = models.ForeignKey(Item, verbose_name=u'商品')
    img = models.ImageField(u'图片', upload_to='images')

    def __unicode__(self):
        return u"%s - %s" % (self.item, self.img)

    class Meta:
        ordering = ['?']