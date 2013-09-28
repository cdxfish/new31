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

        return tuple( i[0] for i in Ord.act[i])


    def saveOrd(self, obj, request):
        from django.contrib.auth.models import User
        from views import OrdSess
        
        o = OrdSess(request).sess

        if o['user']:
            obj.user= User.objects.get(username=o['user'])
        else:
            obj.user = None

        obj.typ = o['typ']
        obj.save()

        return obj

    def cStatus(self, sn , s):
        o = self.get(sn=sn)

        o.status = s

        o.save()

        return o

    def stop(self, sn):

        return self.cStatus(sn, 4)


class Ord(models.Model):
    typs = (
                (0, u'普销'), 
                (1, u'普销(无积分)'), 
                (2, u'活动'), 
                (3, u'积分'), 
            )


    _chcs = (
                (0, u'新单', 'order:copyOrd'), 
                (1, u'编辑', 'order:editOrd'), 
                (2, u'确认', 'order:confirmOrd'),
                (3, u'无效', 'order:nullOrd'),
                (4, u'止单', 'order:stopOrd'),
            )
    chcs= tuple((i[0], i[1]) for i in _chcs)

    act =   ( 
                (_chcs[0], _chcs[1], _chcs[2], _chcs[3], ),
                (_chcs[0], _chcs[1], _chcs[2], _chcs[3], ),
                (_chcs[0], _chcs[4], ),
                (_chcs[0], ),
                (_chcs[0], ),
            )

    sn = models.BigIntegerField(u'订单号', primary_key=True, unique=True)
    user = models.ForeignKey(User, verbose_name=u'会员', blank=True, null=True)
    typ = models.SmallIntegerField(u'订单类型', default=0, choices=typs)
    status = models.SmallIntegerField(u'订单状态', default=0, choices=chcs)

    objects = ordManager()

    def isConfrm(self):

        return self.status == 2


    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.sn, self.user, self.get_typ_display())

    class Meta:
        ordering = ['-sn']
        # verbose_name = u'订单基本信息'