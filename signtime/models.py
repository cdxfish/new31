#coding:utf-8

from django.db import models

# Create your models here.

class SignTimeManager(models.Manager):
    def getTimeById(self, id = ''):

        return SignTime.objects.select_related().get(onl=True, id=id)

    def default(self):

        return self.select_related().filter(onl=True)[0]

    def getTpl(self):
        signTime = SignTime.objects.filter(onl=True)

        a = [(i.id, '%s - %s' % (i.start.strftime('%H: %M'), i.end.strftime('%H: %M'))) for i in signTime]

        return tuple(a)

class SignTime(models.Model):
    start = models.TimeField(u'起始时间')
    end = models.TimeField(u'结束时间')
    onl = models.BooleanField(u'上线')

    objects = SignTimeManager()

    def __unicode__(self):
        return u"%s - %s [ onl: %s ]" % (self.start, self.end, self.onl)