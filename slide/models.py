#coding:utf-8

from django.db import models

# Create your models here.

class Ad(models.Model):
    url = models.CharField(u'链接地址', max_length=60)
    img = models.CharField(u'图片地址', max_length=60)
    show = models.BooleanField(u'是否显示', default=False)
    vieworder = models.SmallIntegerField(u'排序')

    def __unicode__(self):
        return u"%s" % self.img