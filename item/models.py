#coding:utf-8
from django.db import models

# Create your models here.

class itemManager(models.Manager):
    def getBySid(self, id):

        return self.select_related().get(itemspec__id=id, onl=True)

    def getByID(self, id):

        return self.get(id=id, onl=True)

    def likeNameOrSn(self, k):

        return self.select_related().filter((models.Q(name__contains=k) | models.Q(sn__contains=k)) & models.Q(onl=True))


    def getByTag(self, tag):

        return self.select_related().filter(onl=True, tag__tag=tag)


    def getItems(self):

        return self.select_related().filter((models.Q(sn__contains='3133') | models.Q(sn__contains='3155') | models.Q(sn__contains='3177')), onl=True, show=True)

    def getAll(self):

        return self.select_related().filter(onl=True)

class itemSpecManager(models.Manager):
    def getBySid(self, id):

        return self.select_related().get(id=id, onl=True)

    def getByitemID(self, id):

        return self.select_related().filter(item__id=id, item__onl=True, onl=True)

    def default(self):
 
        return self.filter(onl=True)[0]

    def getTpl(self, id):
 
        return ((i.id, i.spec.value) for i in  self.getByitemID(id))


class itemImgManager(models.Manager):
    def getSImgs(self):

        return self.select_related().filter((models.Q(typ=0) | models.Q(typ=1)), onl=True)

    def getBImgs(self):

        return self.select_related().filter((models.Q(typ=2) | models.Q(typ=3)), onl=True)


class itemFeeManager(models.Manager):
    def nomal(self):
        return self.select_related().get(typ=0)

    def nomalAll(self):
        return self.select_related().filter(typ=0)

    def getBySid(self, id):
        return self.select_related().get(spec__id=id, typ=0)


class Item(models.Model):
    from tag.models import Tag
    
    name = models.CharField(u'商品名称', max_length=30, unique=True)
    sn = models.IntegerField(u'货号', unique=True)
    addTime = models.DateTimeField(u'添加时间', auto_now=True, auto_now_add=True)
    onl = models.BooleanField(u'上架', default=False)
    show = models.BooleanField(u'商城可见', default=False)
    like = models.IntegerField(u'喜欢', default=0, editable=False)
    click = models.IntegerField(u'点击', default=0, editable=False)
    tag = models.ManyToManyField(Tag, verbose_name=u'标签', blank=True, null=True)

    objects = itemManager()

    def __unicode__(self):
        return u"%s - %s [ onl: %s ] [ show: %s ]" % (self.name, self.sn, self.onl, self.show)


class ItemDesc(models.Model):
    item = models.ForeignKey(Item, verbose_name=u'商品')
    desc = models.CharField(u'描述', max_length=60)

    def __unicode__(self):
        return u"%s - %s" % (self.item.name, self.desc)

    class Meta:
        ordering = ['?']
        unique_together=(("item","desc"),)     


class ItemSpec(models.Model):
    from spec.models import Spec

    item = models.ForeignKey(Item, verbose_name=u'商品')
    spec = models.ForeignKey(Spec, verbose_name=u'规格')
    onl = models.BooleanField(u'上线', default=False)
    show = models.BooleanField(u'商城可见', default=False)
    objects = itemSpecManager()

    def __unicode__(self):
        return u"%s - %s" % (self.item.name, self.spec)

    class Meta:
        ordering = ['spec']
        unique_together=(("item","spec"),)           


class ItemFee(models.Model):
    from discount.models import Dis

    chcs = ((0,u'零售价'),(1,u'积分换购价'),)
    spec = models.ForeignKey(ItemSpec, verbose_name=u'规格')
    fee = models.DecimalField(u'单价', max_digits=10, decimal_places=2)
    typ = models.SmallIntegerField(u'类型', default=0, choices=chcs)
    dis = models.ForeignKey(Dis, verbose_name=u'折扣')

    objects = itemFeeManager()

    def nfee(self):
        from new31.func import frMtFee
        from decimal import Decimal

        return frMtFee(self.fee * Decimal(self.dis.dis))

    def __unicode__(self):
        return u"%s - %s [ %s ] [ %s ]" % (self.spec, self.fee, self.dis, self.get_typ_display())

    class Meta:
        ordering = ['fee']
        unique_together=(("spec", "typ"),)

class ItemImg(models.Model):
    chcs = ((0, u'188*188'), (1, u'379*188'), (2, u'***450'), (3, u'***960'),)
    item = models.ForeignKey(Item, verbose_name=u'商品')
    img = models.ImageField(u'图片', upload_to='images')
    typ = models.SmallIntegerField(u'类型', default=0, choices=chcs)
    onl = models.BooleanField(u'上线', default=True)
    objects = itemImgManager()

    def __unicode__(self):
        return u"%s - %s[ %s ]" % (self.item.name, self.img, self.get_typ_display())

    class Meta:
        ordering = ['?']
        unique_together=(("img"),)  