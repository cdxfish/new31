#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from item.models import *
from discount.models import *
from new31.func import *

# Create your models here.

class ordLogManager(models.Manager):
    def getlogisBySN(self, sn):

        return self.get(sn=sn)

class ordManager(models.Manager):
    def getOrdByUser(self, user):

        ords = self.select_related(depth=2).filter(user=user)

        for i in ords:
            i.total = OrdItem.objects.getFeeBySN(i.sn)

        return ords

class orderItemManager(models.Manager):
    def getFeeBySN(self, sn):

        ord = OrdInfo.objects.select_related().get(sn=sn)
        total = 0
        for i in ord.orditem_set.all():
            total += forMatFee(i.nfee * i.num)

        return total

class ordSatsManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in OrdSats.act[i]])


class ordPayManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in OrdPay.act[i]])


class ordShipManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in OrdShip.act[i]])


class OrdInfo(models.Model):
    chcs = (
                (0, u'普销'), 
                (1, u'普销(无积分)'), 
                (2, u'活动'), 
                (3, u'积分'), 
                (4, u'提货券'), 
            )

    sn = models.BigIntegerField(u'订单号', primary_key=True, unique=True)
    user = models.ForeignKey(User, verbose_name=u'会员', blank=True, null=True)
    typ = models.SmallIntegerField(u'订单类型', default=0, choices=chcs)

    objects = ordManager()

    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.sn, self.user, self.get_typ_display())

    class Meta:
        ordering = ['-sn']
        # verbose_name = u'订单基本信息'


class OrdLog(models.Model):
    chcs = (
            (0, u'新单'),
            (1, u'编辑'),
            (2, u'确认'),
            (3, u'取消'),
            (4, u'无效'),
            (5, u'完成'),
            (6, u'停止'),
            (7, u'发货'),
            (8, u'签收'),
            (9, u'拒签'),
            (10, u'付款'),
        )

    ord = models.ForeignKey(OrdInfo, verbose_name=u'订单')
    user = models.ForeignKey(User, verbose_name=u'用户')
    log = models.SmallIntegerField(u'日志类型', default=0, choices=chcs)
    note = models.CharField(u'备注', max_length=60, blank=True, null=True)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % ( self.ord, self.get_log_display(), self.time )
        
    class Meta:
        unique_together=(("ord","time"),)
        # verbose_name = u'订单日志'
        # 记录类似于下单时间.付款时间.发货时间等             


class OrdLogcs(models.Model):
    chcs = (
            (-3, '- 90 m'),
            (-2, '- 60 m'),
            (-1, '- 30 m'),
            (0, '0 m'),
            (1, '+ 30 m'),
            (2, '+ 60 m'),
            (3, '+ 90 m'),
        )
    ord = models.OneToOneField(OrdInfo, verbose_name=u'订单')
    consignee = models.CharField(u'收货人', max_length=60)
    area = models.CharField(u'配送区域', max_length=60)
    address = models.CharField(u'详细地址', max_length=255)
    tel = models.CharField(u'联系电话', max_length=60)
    date = models.DateField(u'收货日期')
    stime = models.TimeField(u'起始时间')
    etime = models.TimeField(u'结束时间')
    lstime = models.TimeField(u'物流起始时间')
    letime = models.TimeField(u'物流结束时间')
    advance = models.SmallIntegerField(u'提前量', default=0, choices=chcs)
    dman = models.ForeignKey(User, verbose_name=u'物流师傅', blank=True, null=True)
    note = models.CharField(u'备注', max_length=255, blank=True, null=True)

    objects = ordLogManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s  %s - %s ][ %s ][ %s ]" % ( self.ord, self.consignee, self.date, self.stime, self.etime, self.tel, self.dman )
        
    # class Meta: 
        # verbose_name = u'订单物流信息'             


class OrdSats(models.Model):
    chcs = (
                (0, u'新单'), 
                (1, u'编辑'), 
                (2, u'确认'),
                (3, u'无效'),
                (4, u'止单'),
            )

    act =   ( 
                ((0, u'新单'),(1, u'编辑'),(2, u'确认'),(3, u'无效'),),
                ((0, u'新单'),(1, u'编辑'),(2, u'确认'),(3, u'无效'),),
                ((0, u'新单'),(4, u'止单'),),
                ((0, u'新单'),),
                ((0, u'新单'),),
            )

    ord = models.OneToOneField(OrdInfo, verbose_name=u'订单')
    status = models.SmallIntegerField(u'订单状态', default=0, editable=False, choices=chcs)

    objects = ordSatsManager()

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.ord, self.get_status_display() )    

    # class Meta:
        # verbose_name = u'订单支付'


class OrdPay(models.Model):
    from payment.models import Pay
    chcs = (
                (0, u'未付'), 
                (1, u'已付'),
                (2, u'已结'),
                (3, u'已核'),
            )

    act =   (
                ((1, u'已付'),),
                ((2, u'已结'),),
                ((3, u'已核'),),
                (),
        )

    ord = models.OneToOneField(OrdInfo, verbose_name=u'订单')
    cod = models.ForeignKey(Pay, verbose_name=u'支付方式')
    status = models.SmallIntegerField(u'支付状态', default=0, editable=False, choices=chcs)

    objects = ordPayManager()

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.ord, self.name, self.get_status_display() )

    # class Meta:
        # verbose_name = u'订单支付'


class OrdShip(models.Model):
    chcs = (
                (0, u'未发'),
                (1, u'编辑'),
                (2, u'已发'), 
                (3, u'拒签'), 
                (4, u'已签'), 
                (5, u'止送'), 
            )
    act =   (
                ((1, u'编辑'), (2, u'已发'),(5, u'止送'), ),
                ((1, u'编辑'), (2, u'已发'),(5, u'止送'), ),
                ((3, u'拒签'),(4, u'已签'),),
                (),
                (),
                (),
            )
    ord = models.OneToOneField(OrdInfo, verbose_name=u'订单')
    name = models.CharField(u'物流方式', max_length=30, editable=False)
    cod = models.CharField(u'代码', max_length=30)
    status = models.SmallIntegerField(u'物流状态', default=0, editable=False, choices=chcs)

    objects = ordShipManager()

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.ord, self.name, self.get_status_display() )    

    # class Meta:
        # verbose_name = u'订单物流'


class OrdItem(models.Model):
    ord = models.ForeignKey(OrdInfo, verbose_name=u'订单')
    name = models.CharField(u'商品', max_length=30)
    sn = models.CharField(u'货号', max_length=30)
    spec = models.CharField(u'规格', max_length=30)
    num = models.SmallIntegerField(u'数量')
    typ = models.SmallIntegerField(u'商品类型', default=0, choices=ItemFee.chcs)
    fee = models.DecimalField(u'原价', max_digits=10, decimal_places=2)
    nfee = models.DecimalField(u'现价', max_digits=10, decimal_places=2)
    dis = models.FloatField(u'折扣', default=1.0, choices=Discount.chcs)

    objects = orderItemManager()

    def __unicode__(self):
        return u"%s - %s[ %s ][ %s ][ %d ]" % ( self.ord, self.name, self.spec, self.num, self.fee )