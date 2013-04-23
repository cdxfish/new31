#coding:utf-8
from django.db import models

# Create your models here.

class OrderInfo(models.Model):
    orderSn = models.BigIntegerField(u'订单号', primary_key=True, unique=True)
    user = models.CharField(u'会员', max_length=30, blank=True, null=True)
    note = models.CharField(u'备注', max_length=255, blank=True, null=True)
    referer = models.CharField(u'订单来源', max_length=30)
    orderType = models.SmallIntegerField(u'订单类型', choices=((1,u'普通销售订单'), (2,u'活动订单'),),default=1,)

    def __unicode__(self):
        return u"%s" % self.orderSn

    class Meta:
        ordering = ['-orderSn']
        # verbose_name = u'订单基本信息'


class OrderLog(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    orderStatus = models.SmallIntegerField(u'订单状态(操作前)', default=0, editable=False)
    user = models.CharField(u'管理员', max_length=30, editable=False)
    actionType = models.SmallIntegerField(u'操作', editable=False)
    note = models.CharField(u'备注', max_length=255, blank=True, null=True)
    logTime = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"%s - [a:%s][%s]" % ( self.order, self.actionType, self.logTime )
        
    class Meta:
        unique_together = (("order","actionType"),)
        # verbose_name = u'订单日志'


class OrderLineTime(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    timeType = models.SmallIntegerField(u'时间类型')
    lineTime = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u"%s - [t:%s][%s]" % ( self.order, self.timeType, self.lineTime )
        
    class Meta:
        unique_together=(("order","timeType"),)   
        # verbose_name = u'订单时间线'
        # 记录类似于下单时间.付款时间.发货时间等             


class OrderLogistics(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    consignee = models.CharField(u'联系人', max_length=60)
    area = models.CharField(u'配送区域', max_length=60)
    address = models.CharField(u'地址', max_length=255)
    tel = models.CharField(u'联系电话', max_length=60)
    signDate = models.DateField(u'收货日期')
    signTimeStart = models.TimeField(u'起始时间')
    signTimeEnd = models.TimeField(u'结束时间')
    logisDate = models.DateField(u'物流日期')
    logisTime = models.CharField(u'物流时间', max_length=60)
    deliveryman = models.CharField(u'物流师傅', max_length=60)

    def __unicode__(self):
        return u"%s - [c:%s][%s:%s - %s ][%s]" % ( self.order, self.consignee, self.signDate, self.signTime, self.signTimeEnd, self.tel )
        
    # class Meta: 
        # verbose_name = u'订单物流信息'             


class OrderStatus(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    orderStatus = models.SmallIntegerField(u'订单状态', default=0, editable=False)

    def __unicode__(self):
        return u"%s - [o:%s]" % ( self.order, self.orderStatus )    

    # class Meta:
        # verbose_name = u'订单支付'


class OrderPay(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    payName = models.CharField(u'支付方式', max_length=30)
    payStatus = models.SmallIntegerField(u'支付状态', default=0, editable=False)

    def __unicode__(self):
        return u"%s - %s[p:%s]" % ( self.order, self.payName, self.payStatus )    

    # class Meta:
        # verbose_name = u'订单支付'


class OrderShip(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    shipName = models.CharField(u'物流方式', max_length=30, editable=False)
    shipStatus = models.SmallIntegerField(u'物流状态', default=0, editable=False)

    def __unicode__(self):
        return u"%s - %s[p:%s]" % ( self.order, self.payName, self.payStatus )    

    # class Meta:
        # verbose_name = u'订单物流'


class OrderItem(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单', db_column='order')
    item = models.CharField(u'商品', max_length=30)
    sn = models.CharField(u'货号', max_length=30)

    def __unicode__(self):
        return u"%s - %s[%s]" % ( self.order, self.item, self.sn )    

    class Meta:
        unique_together = (("order","item"),)
        # verbose_name = u'订单商品'


class OrderSpec(models.Model):
    item = models.ForeignKey(OrderItem, verbose_name=u'商品')
    spec = models.CharField(u'规格', max_length=30)

    def __unicode__(self):
        return u"%s - %s" % ( self.item, self.spec )

    class Meta:
        unique_together = (("item","spec"),)
        # verbose_name = u'订单商品规格'


class OrderFee(models.Model):
    itemSpec = models.ForeignKey(OrderSpec, verbose_name=u'规格')
    number = models.SmallIntegerField(u'数量')
    itemType = models.SmallIntegerField(u'商品类型')
    amount = models.DecimalField(u'单价', max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u"%s - [n:%s][t:%s][a:%s]" % ( self.itemSpec, self.number, self.itemType, self.amount )
    class Meta:
        unique_together = (("itemSpec","itemType"),)
        # verbose_name = u'订单商品价格'


class OrderDiscount(models.Model):
    itemSpec = models.ForeignKey(OrderFee, verbose_name=u'商品', unique=True)
    discount = models.DecimalField(u'折扣', max_digits=3, decimal_places=1)


    def __unicode__(self):
        return u"%s - %s折" % ( self.itemSpec, self.discount )

    # class Meta:
        # verbose_name = u'订单商品折扣'

