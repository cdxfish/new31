#coding:utf-8

from django.db import models

# Create your models here.

class SignTimeManager(models.Manager):
    def getTimeById(self, id = ''):

        return SignTime.objects.select_related().get(onLine=True, id=id)

    def getDefault(self):

        return self.select_related().filter(onLine=True)[0]

    def  getTupleByAll(self):
        signTime = SignTime.objects.filter(onLine=True)

        a = [(i.id, '%s - %s' % (i.start.strftime('%H: %M'), i.end.strftime('%H: %M'))) for i in signTime]

        return tuple(a)

class SignTime(models.Model):
    start = models.TimeField(u'起始时间')
    end = models.TimeField(u'结束时间')
    onLine = models.BooleanField(u'上线')

    objects = SignTimeManager()

    def __unicode__(self):
        return u"%s - %s [ onLine: %s ]" % (self.start, self.end, self.onLine)