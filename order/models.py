#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from item.models import *
from discount.models import *
from new31.func import *

# Create your models here.

class ordManager(models.Manager):
    def getByUser(self, user):

        return self.select_related(depth=2).filter(user=user)

    def lenNewOrd(self, user):

        return len(self.filter((models.Q(status=0) | models.Q(status=1)), user=user))

    def getActTuple(self, i):

        return tuple([ i for i, v in Ord.act[i]])


    def saveOrd(self, ord, request):
        from django.contrib.auth.models import User
        from views import OrdSess
        
        o = OrdSess(request).sess
        print o
        if o['user']:
            ord.user= User.objects.get(username=o['user'])
        else:
            ord.user = None

        ord.typ = o['typ']
        ord.save()

    def cStatus(self, sn , s):
        ord = self.get(sn=sn)

        ord.status = s

        ord.save()

    def stop(self, sn):

        return self.cStatus(sn, 4)


class Ord(models.Model):
    typs = (
                (0, u'普销'), 
                (1, u'普销(无积分)'), 
                (2, u'活动'), 
                (3, u'积分'), 
                (4, u'提货券'), 
            )


    chcs = (
                (0, u'新单'), 
                (1, u'编辑'), 
                (2, u'确认'),
                (3, u'无效'),
                (4, u'止单'),
            )

    act =   ( 
                ((0, u'新单'),(1, u'编辑'),(2, u'确认'),(3, u'无效'),),
                ((0, u'新单'),(1, u'编辑'),(2, u'确认'),(3, u'无效'),),
                ((0, u'新单'),(4, u'止单'),),
                ((0, u'新单'),),
                ((0, u'新单'),),
            )


    sn = models.BigIntegerField(u'订单号', primary_key=True, unique=True)
    user = models.ForeignKey(User, verbose_name=u'会员', blank=True, null=True)
    typ = models.SmallIntegerField(u'订单类型', default=0, choices=typs)
    status = models.SmallIntegerField(u'订单状态', default=0, editable=False, choices=chcs)


    objects = ordManager()

    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.sn, self.user, self.get_typ_display())

    class Meta:
        ordering = ['-sn']
        # verbose_name = u'订单基本信息'