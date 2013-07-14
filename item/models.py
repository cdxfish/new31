#coding:utf-8

from django.db import models
from django.db.models import Q
from tag.models import *
from spec.models import *
from discount.models import *

# Create your models here.

class itemManager(models.Manager):
    def getItemByItemName(self, itemName = ''):

        return self.select_related().get(name=itemName, onLine=True)

    def getTagByItemName(self, itemName = ''):

        return self.select_related().get(name=itemName, onLine=True).tag.all()

    def getItemBySpecId(self, id = 0):

        item = ItemSpec.objects.select_related().get(id=id, onLine=True, show=True).item

        if item.onLine and item.show:

            return item
        else:

            raise item.DoesNotExist

    def getItemByItemID(self, id = 0):

        return self.get(id=id, onLine=True, show=True)

    def getItemLikeNameOrSn(self, k):

        return self.select_related().filter((Q(name__contains=k) | Q(sn__contains=k)) & Q(onLine=True))

    def getItemByAll(self):

        return self.select_related().filter(onLine=True, show=True)

    def getItemByTag(self, tag):

        return Tag.objects.getTagByTagTitle(tag).item_set.filter(onLine=True)

    def getShowItemByTag(self, tag):

        return Tag.objects.getTagByTagTitle(tag).item_set.filter(onLine=True,show=True)

    def getItemByRandom(self):

        return self.select_related().filter(onLine=True,show=True).order_by('?')[0]

    def getItems(self):

        return self.select_related().filter((Q(sn__contains='3133') | Q(sn__contains='3155') | Q(sn__contains='3177')), onLine=True, show=True)


class itemDescManager(models.Manager):
    def random(self, itemName = ''):

        return self.select_related().all()[0]


class itemSpecManager(models.Manager):
    def getSpecBySpecID(self, id):

        return self.select_related().get(id=id, onLine=True, show=True)

    def getSpecByItemID(self, id):

        return Item.objects.select_related().get(id=int(id), onLine=True, show=True).itemspec_set.filter(onLine=True)

    def getDefaultSpec(self):
 
        return self.filter(onLine=True)[0]

    def getTupleByItemID(self, id):
 
        return ((i.id, i.spec.value) for i in  self.getSpecByItemID(id))


class itemImgManager(models.Manager):
    def getImgByAll(self):

        return self.all()

    def getSImgs(self):

        return self.select_related().filter(iType=0, onLine=True)


class itemFeeManager(models.Manager):
    def getFeeByNomal(self):
        return self.select_related().get(itemType=0)

    def getAllFeeByNomal(self):
        return self.select_related().filter(itemType=0)

    def getFeeBySpecID(self, specID):
        return ItemSpec.objects.getSpecBySpecID(id=specID).itemfee_set.getAllFeeByNomal()[0]

    def getTupleBySpecID(self, id):
        itemFees = self.getFeeBySpecID(id)

        return ((i.itemdiscount.discount.id, i.itemdiscount.discount.get_discount_display()) for i in  itemFees)


class itemDisManager(models.Manager):
    def getDisBySpecID(self, specID):

        return ItemSpec.objects.getSpecBySpecID(id=specID).itemfee_set.getFeeByNomal().itemdiscount.discount

    def getDisByDisID(self, disID):

        return self.get(id=disID).discount


class Item(models.Model):
    name = models.CharField(u'商品名称', max_length=30, unique=True)
    sn = models.IntegerField(u'货号', unique=True)
    addTime = models.DateTimeField(u'添加时间', auto_now=True, auto_now_add=True)
    onLine = models.BooleanField(u'上架', default=False)
    show = models.BooleanField(u'商城可见', default=False)
    like = models.IntegerField(u'喜欢', default=0, editable=False)
    click = models.IntegerField(u'点击', default=0, editable=False)
    tag = models.ManyToManyField(Tag, verbose_name=u'标签', blank=True, null=True)

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
    itemTypeChoices = ((0,u'零售价'),(1,u'积分换购价'),)
    itemSpec = models.ForeignKey(ItemSpec, verbose_name=u'规格', unique=True)
    amount = models.DecimalField(u'单价', max_digits=10, decimal_places=2)
    itemType = models.SmallIntegerField(u'类型', default=0, choices=itemTypeChoices)

    objects = itemFeeManager()

    def __unicode__(self):
        return u"%s - %s [%s]" % (self.itemSpec, self.amount, self.get_itemType_display())

    class Meta:
        ordering = ['amount']
        unique_together=(("itemSpec","amount","itemType"),)   


class ItemDiscount(models.Model):
    itemFee = models.OneToOneField(ItemFee, verbose_name=u'单价', unique=True)
    discount = models.ForeignKey(Discount, verbose_name=u'折扣')

    objects = itemDisManager()

    def __unicode__(self):
        return u"%s - %s" % (self.itemFee, self.discount)


class ItemImg(models.Model):
    iTypeChoices = ((0,u'小图'),(1,u'大图'),)
    item = models.ForeignKey(Item, verbose_name=u'商品')
    img = models.ImageField(u'图片', upload_to='images')
    iType = models.SmallIntegerField(u'类型', default=0, choices=iTypeChoices)
    onLine = models.BooleanField(u'上线', default=True)
    objects = itemImgManager()

    def __unicode__(self):
        return u"%s - %s" % (self.item, self.img)

    class Meta:
        ordering = ['?']
        unique_together=(("img"),)  