#coding:utf-8
from django.db import models

# Create your models here.

class logcsManager(models.Manager):
    def getlogcsBySN(self, sn):

        return self.get(sn=sn)

    def getActTuple(self, i):

        return tuple([ i[0] for i in Logcs.act[i]])


    def saveLogcs(self, ord, request):
        from views import LogcSess

        c = LogcSess(request).getObj()
        avd = 1 # 默认偏移1hour

        time = c['time']

        area = c['area']
        try:
            logcs = ord.logcs
        except Exception, e:
            logcs = Logcs()

        logcs.ord = ord

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

        logcs.save()

    def cStatus(self, sn , s):
        logcs = self.get(ord=sn)

        logcs.status = s

        logcs.save()

    def stop(self, sn):

        return self.cStatus(sn, 5)

    def getAll(self):

        return self.select_related().filter(ord__status__gt=1)



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

    _chcs = (
                (0, u'未发', 'logistics:logcsUnsent'),
                (1, u'编辑', 'logistics:logcsEdit'),
                (2, u'已发', 'logistics:logcsShip'), 
                (3, u'拒签', 'logistics:logcsRefused'), 
                (4, u'已签', 'logistics:logcsSign'), 
                (5, u'止送', 'logistics:logcsStop'), 
        )
    chcs= tuple((i[0],i[1]) for i in _chcs)

    act =   (
                (_chcs[0], _chcs[1], _chcs[2], _chcs[5], ),
                (_chcs[0], _chcs[1], _chcs[2], _chcs[5], ),
                (_chcs[0], _chcs[3], _chcs[4], ),
                (_chcs[0], ),
                (_chcs[0], ),
                (_chcs[0], ),
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
    cod = models.ForeignKey(Deliver, verbose_name=u'送货方式')
    status = models.SmallIntegerField(u'物流状态', default=0, choices=chcs)

    def ltime(self):

        return u'%s - %s' % ( self.stime.strftime('%H:%M'), self.etime.strftime('%H:%M') )

    def advTime(self):

        time = self.advance * 0.5
        hour = self.lstime.hour + int(time)
        minute = 30 if (time % 1) else 0

        if self.advance < 0 and time % 1:
            hour -= 1

        # e = datetime.timedelta(hour=i.logcs.advance * 0.5)

        return self.lstime.replace(hour=hour, minute=minute)

    objects = logcsManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s  %s - %s ][ %s ][ %s ]" % ( self.ord, self.consignee, self.date, self.stime, self.etime, self.tel, self.dman )
        
    # class Meta: 
        # verbose_name = u'订单物流信息' 