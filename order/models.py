#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from item.models import *
from discount.models import *

# Create your models here.

class orderLogisticsManager(models.Manager):
    def getlogisBySN(self, sn):

        return self.get(sn=sn)


class OrderInfo(models.Model):
    oType = (
                (0, u'普销'), 
                (1, u'普销(无积分)'), 
                (2, u'活动'), 
                (3, u'积分'), 
                (4, u'提货券'), 
            )
    sn = models.BigIntegerField(u'订单号', primary_key=True, unique=True)
    user = models.OneToOneField(User, verbose_name=u'会员', blank=True, null=True)
    orderType = models.SmallIntegerField(u'订单类型', default=0, choices=oType)

    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.sn, self.user, self.get_orderType_display())

    class Meta:
        ordering = ['-sn']
        # verbose_name = u'订单基本信息'


class OrderLog(models.Model):
    logType = (
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

    order = models.ForeignKey(OrderInfo, verbose_name=u'订单')
    user = models.ForeignKey(User, verbose_name=u'用户')
    log = models.SmallIntegerField(u'日志类型', default=0, choices=logType)
    note = models.CharField(u'备注', max_length=60, blank=True, null=True)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % ( self.order, self.get_log_display(), self.time )
        
    class Meta:
        unique_together=(("order","time"),)   
        # verbose_name = u'订单日志'
        # 记录类似于下单时间.付款时间.发货时间等             


class OrderLogistics(models.Model):
    aChoice = (
            (-3, '- 90 m'),
            (-2, '- 60 m'),
            (-1, '- 30 m'),
            (0, '0 m'),
            (1, '+ 30 m'),
            (2, '+ 60 m'),
            (3, '+ 90 m'),
        )
    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    consignee = models.CharField(u'收货人', max_length=60)
    area = models.CharField(u'配送区域', max_length=60)
    address = models.CharField(u'详细地址', max_length=255)
    tel = models.CharField(u'联系电话', max_length=60)
    signDate = models.DateField(u'收货日期')
    signTimeStart = models.TimeField(u'起始时间')
    signTimeEnd = models.TimeField(u'结束时间')
    logisTimeStart = models.TimeField(u'物流起始时间')
    logisTimeEnd = models.TimeField(u'物流结束时间')
    advance = models.SmallIntegerField(u'提前量', default=0, choices=aChoice)
    dman = models.OneToOneField(User, verbose_name=u'物流师傅', blank=True, null=True)
    note = models.CharField(u'备注', max_length=255, blank=True, null=True)

    objects = orderLogisticsManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s  %s - %s ][ %s ]" % ( self.order, self.consignee, self.signDate, self.signTimeStart, self.signTimeEnd, self.tel )
        
    # class Meta: 
        # verbose_name = u'订单物流信息'             


class OrderStatus(models.Model):
    oStatus = (
                (0, u'新单'), 
                (1, u'编辑'), 
                (2, u'确认'),
                (3, u'无效'),
                (4, u'停止'),
                (5, u'完成'),
            )

    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    status = models.SmallIntegerField(u'订单状态', default=0, editable=False, choices=oStatus)

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.order, self.get_orderStatus_display() )    

    # class Meta:
        # verbose_name = u'订单支付'


class OrderPay(models.Model):
    oStatus = (
                (0, u'未付'), 
                (1, u'已付'),
                (2, u'已结'),
                (3, u'已核'),
            )

    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    name = models.CharField(u'支付方式', max_length=30)
    cod = models.CharField(u'代码', max_length=30)
    status = models.SmallIntegerField(u'支付状态', default=0, editable=False, choices=oStatus)

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.order, self.name, self.get_payStatus_display() )

    # class Meta:
        # verbose_name = u'订单支付'


class OrderShip(models.Model):
    oStatus = (
                (0, u'未发'),
                (1, u'编辑'),
                (2, u'已发'), 
                (3, u'拒签'), 
                (4, u'已签'), 
            )

    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    name = models.CharField(u'物流方式', max_length=30, editable=False)
    cod = models.CharField(u'代码', max_length=30)
    status = models.SmallIntegerField(u'物流状态', default=0, editable=False, choices=oStatus)

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.order, self.name, self.get_shipStatus_display() )    

    # class Meta:
        # verbose_name = u'订单物流'


class OrderItem(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单')
    name = models.CharField(u'商品', max_length=30)
    sn = models.CharField(u'货号', max_length=30)
    spec = models.CharField(u'规格', max_length=30)
    number = models.SmallIntegerField(u'数量')
    itemType = models.SmallIntegerField(u'商品类型', default=0, choices=ItemFee.itemTypeChoices)
    amount = models.DecimalField(u'原价', max_digits=10, decimal_places=2)
    nowFee = models.DecimalField(u'现价', max_digits=10, decimal_places=2)
    discount = models.FloatField(u'折扣', default=1.0, choices=Discount.disChoices)

    def __unicode__(self):
        return u"%s - %s[ %s ][ %s ][ %d ]" % ( self.order, self.name, self.spec, self.number, self.amount )