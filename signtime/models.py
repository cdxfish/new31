#coding:utf-8

from django.db import models

# Create your models here.

class SignTime(models.Model):
    value = models.CharField(u'收货时间', max_length=60, unique=True)
    isOpen = models.BooleanField(u'是否可选', max_length=60)
    vieworder = models.SmallIntegerField(u'排序')

    def __unicode__(self):
        return u"%s" % self.value