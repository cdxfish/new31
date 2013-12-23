#coding:utf-8
from django.db import models

# Create your models here.

class PayManager(models.Manager):
    def getPayById(self, id = ''):

        return self.select_related().get(onl=True, id=id)

    def default(self):

        return self.select_related().filter(onl=True)[0]

    def getTpl(self):

        return tuple([(i.id, i.get_cod_display()) for i in self.filter(onl=True)])

    def getTplToShow(self):

        return tuple([(i.id, i.get_cod_display()) for i in self.filter(cod__in=['payafter', 'alipay', 'post'], onl=True)])

class APIBase(object):
    u"""支付插件基本类"""

    urls = ()
    conf = ()

    def __init__(self, ord, request, *args, **kwargs):
        self.ord = ord
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def submit(self):

        return self

    def paid(self):
        u"""订单支付"""
        self.ord.user.pts.set(self.ord.pro_set.all().pts())

        return self

    def reimburse(self):
        u"""订单退付"""
        self.ord.user.pts.set(-self.ord.pro_set.all().pts())

        return self

    def postUrl(self):

        return ''


class Pay(models.Model):
    import api

    chcs = tuple( [ (i, api.__dict__[i].__doc__, ) for i in dir(api) if i[0] != '_' ] )

    cod = models.CharField(u'代码', max_length=30, choices=chcs)
    config = models.TextField(u'配置')
    onl = models.BooleanField(u'上线')

    def _config(self):
        import json
        return json.loads(self.config)

    objects = PayManager()

    def __init__(self, *args, **kwargs):
        super(Pay, self).__init__(*args, **kwargs)

        self.main = type('Main', (getattr(self.api, self.cod).Main, APIBase,), self._config())

    def __unicode__(self):
        return u"%s - %s [ %s ]" % (self.get_cod_display(), self.cod, self.onl)

    class Meta:
        verbose_name = u'支付方式'