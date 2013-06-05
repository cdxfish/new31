#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from item.models import *

# Create your models here.

class OrderInfo(models.Model):
    oType = ((0,u'普销'), (1,u'普销(无积分)'), (2,u'活动'), (3,u'积分'), (4,u'提货券'), )
    orderSn = models.BigIntegerField(u'订单号', primary_key=True, unique=True)
    user = models.CharField(u'会员', max_length=30, blank=True, null=True)
    referer = models.CharField(u'订单来源', max_length=30)
    orderType = models.SmallIntegerField(u'订单类型', default=0, choices=oType,)

    def __unicode__(self):
        return u"%s [ %s ][ %s ] - %s" % (self.orderSn, self.user, self.referer, self.get_orderType_display())

    class Meta:
        ordering = ['-orderSn']
        # verbose_name = u'订单基本信息'


class OrderLog(models.Model):
    aType = (
                (0,u'确认'),
            )

    order = models.ForeignKey(OrderInfo, verbose_name=u'订单')
    user = models.ForeignKey(User, verbose_name=u'用户')
    actionType = models.SmallIntegerField(u'操作', editable=False, choices=aType)
    note = models.CharField(u'备注', max_length=60, blank=True, null=True)
    logTime = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"%s - [a:%s][%s]" % ( self.order, self.get_actionType_display(), self.logTime )
        
    class Meta:
        unique_together = (("order","actionType"),)
        # verbose_name = u'订单日志'


class OrderLineTime(models.Model):
    tT = (
            (0, u'下单'),
            (1, u'确认'),
            (2, u'取消'),
            (3, u'无效'),
            (4, u'完成'),
            (5, u'停止'),
            (6, u'发货'),
            (7, u'签收'),
            (8, u'拒签'),
            (9, u'付款'),
        )

    order = models.ForeignKey(OrderInfo, verbose_name=u'订单')
    timeType = models.SmallIntegerField(u'时间类型', default=0, choices=tT)
    lineTime = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % ( self.order, self.get_timeType_display(), self.lineTime )
        
    class Meta:
        unique_together=(("order","timeType"),)   
        # verbose_name = u'订单时间线'
        # 记录类似于下单时间.付款时间.发货时间等             


class OrderLogistics(models.Model):
    advanceChoice = (
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
    advance = models.SmallIntegerField(u'提前量', default=0, choices=advanceChoice)
    deliveryman = models.CharField(u'物流师傅', max_length=60, blank=True, null=True)
    note = models.CharField(u'备注', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u"%s - [ %s ][ %s  %s - %s ][ %s ]" % ( self.order, self.consignee, self.signDate, self.signTimeStart, self.signTimeEnd, self.tel )
        
    # class Meta: 
        # verbose_name = u'订单物流信息'             


class OrderStatus(models.Model):
    oStatus = (
                (0, u'新单'), 
                (1, u'确认'), 
                (2, u'编辑'),
                (3, u'无效'),
                (4, u'完成'),
                (5, u'停止'),
                (6, u'重建'),
                (7, u'更换'),
            )

    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    orderStatus = models.SmallIntegerField(u'订单状态', default=0, editable=False, choices=oStatus)

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.order, self.get_orderStatus_display() )    

    # class Meta:
        # verbose_name = u'订单支付'


class OrderPay(models.Model):
    pStatus = (
                (0, u'未付'), 
                (1, u'已付'),
            )

    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    payName = models.CharField(u'支付方式', max_length=30)
    cod = models.CharField(u'代码', max_length=30)
    payStatus = models.SmallIntegerField(u'支付状态', default=0, editable=False, choices=pStatus)

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.order, self.payName, self.get_payStatus_display() )

    # class Meta:
        # verbose_name = u'订单支付'


class OrderShip(models.Model):
    sStatus = (
                (0, u'未发'), 
                (1, u'已发'), 
                (2, u'拒签'), 
                (3, u'已签'), 
            )

    order = models.OneToOneField(OrderInfo, verbose_name=u'订单')
    shipName = models.CharField(u'物流方式', max_length=30, editable=False)
    cod = models.CharField(u'代码', max_length=30)
    shipStatus = models.SmallIntegerField(u'物流状态', default=0, editable=False, choices=sStatus)

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.order, self.shipName, self.get_shipStatus_display() )    

    # class Meta:
        # verbose_name = u'订单物流'


class OrderItem(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单')
    name = models.CharField(u'商品', max_length=30)
    sn = models.CharField(u'货号', max_length=30)
    spec = models.CharField(u'规格', max_length=30)
    number = models.SmallIntegerField(u'数量')
    itemType = models.SmallIntegerField(u'商品类型', default=0, choices=ItemFee.itemTypeChoices)
    amount = models.DecimalField(u'单价', max_digits=10, decimal_places=2)
    discount = models.DecimalField(u'折扣', max_digits=3, decimal_places=1, default=10.0)

    def __unicode__(self):
        return u"%s - %s[ %s ][ %s ][ %d ]" % ( self.order, self.name, self.spec, self.number, self.amount )