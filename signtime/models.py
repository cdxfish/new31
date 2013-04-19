#coding:utf-8

from django.db import models

# Create your models here.

class SignTime(models.Model):
    start = models.TimeField(u'起始时间')
    end = models.TimeField(u'结束时间')
    onLine = models.BooleanField(u'上线')

    def __unicode__(self):
        return u"%s - %s [ onLine: %s ]" % (self.start, self.end, self.onLine)