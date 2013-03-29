#coding:utf-8
from django.db import models

# Create your models here.

class Pay(models.Model):
    name = models.CharField(u'名字', max_length=30)
    cod = models.CharField(u'代码', max_length=30)
    config = models.TextField(u'配置')
    onLine = models.BooleanField(u'上线')

    def __unicode__(self):
        return u"%s - %s" % (self.name, slef.onLine)

    # class Meta:
        # verbose_name = u'支付方式'