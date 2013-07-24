#coding:utf-8
from django.db import models

# Create your models here.

class logcsManager(models.Manager):
    def getlogcsBySN(self, sn):

        return self.get(sn=sn)

    def getActTuple(self, i):

        return tuple([ i for i, v in OrdLogcs.act[i]])


    def saveLogcs(self, ord, request):
        from views import Cnsgn

        c = Cnsgn(request).getObj()
        avd = 1 # 默认偏移1hour

        time = c['time']

        area = c['area']

        logcs = Logcs()
        logcs.consignee = c['consignee']
        logcs.area = '%s - %s' % (area.sub.name, area.name)
        logcs.address = c['address']
        logcs.tel = c['tel']
        logcs.date = c['date']
        logcs.stime = time.start
        logcs.etime = time.end
        logcs.lstime = time.start.replace(hour = time.start.hour - avd)
        logcs.letime = time.end.replace(hour = time.end.hour - avd)
        logcs.note = c['note']
        logcs.cod = c['dlvr']

        logcs.ord = ord

        logcs.save()

class Logcs(models.Model):
    from django.contrib.auth.models import User
    from deliver.models import Deliver
    from order.models import Ord
    advs = (
                (-3, '- 90 m'),
                (-2, '- 60 m'),
                (-1, '- 30 m'),
                (0, '0 m'),
                (1, '+ 30 m'),
                (2, '+ 60 m'),
                (3, '+ 90 m'),
        )

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


    ord = models.OneToOneField(Ord, verbose_name=u'订单')
    consignee = models.CharField(u'收货人', max_length=60)
    area = models.CharField(u'配送区域', max_length=60)
    address = models.CharField(u'详细地址', max_length=255)
    tel = models.CharField(u'联系电话', max_length=60)
    date = models.DateField(u'收货日期')
    stime = models.TimeField(u'起始时间')
    etime = models.TimeField(u'结束时间')
    lstime = models.TimeField(u'物流起始时间')
    letime = models.TimeField(u'物流结束时间')
    advance = models.SmallIntegerField(u'提前量', default=0, choices=advs)
    dman = models.ForeignKey(User, verbose_name=u'物流师傅', blank=True, null=True)
    note = models.CharField(u'备注', max_length=255, blank=True, null=True)
    # pcod = models.ForeignKey(Pay, verbose_name=u'支付方式')
    # dcod = models.ForeignKey(Deliver, verbose_name=u'送货方式')
    cod = models.ForeignKey(Deliver, verbose_name=u'送货方式')
    status = models.SmallIntegerField(u'物流状态', default=0, editable=False, choices=chcs)

    objects = logcsManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s  %s - %s ][ %s ][ %s ]" % ( self.ord, self.consignee, self.date, self.stime, self.etime, self.tel, self.dman )
        
    # class Meta: 
        # verbose_name = u'订单物流信息' 