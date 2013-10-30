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


class Pay(models.Model):
    import api

    chcs = tuple( [ (i, api.__dict__[i].__doc__, ) for i in dir(api) if i[0] != '_' ] )

    cod = models.CharField(u'代码', max_length=30, choices=chcs)
    config = models.TextField(u'配置')
    onl = models.BooleanField(u'上线')

    objects = PayManager()

    def sub(self, ord):
        try:
            getattr(self.api, self.cod).main(ord).sub()
        except Exception, e:
            raise e

        return self
    
    def pay(self, ord):
        getattr(self.api, self.cod).main(ord).pay()

        return self
    
    def re(self, ord):
        getattr(self.api, self.cod).main(ord).re()

        return self

    def __unicode__(self):
        return u"%s - %s" % (self.get_cod_display(), self.onl)

    class Meta:
        verbose_name = u'支付方式'