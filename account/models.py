#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from new31.decorator import timeit
# Create your models here.

class bsInfoManager(models.Manager):
    def set(self, request):

        u = request.user.bsinfo

        if not u.sex:
            u.sex = request.POST.get('sex')
        else:
            u.sex = u.sex
            messages.warning(request, u'无法再次修改性别')

        if not u.mon:
            u.mon = request.POST.get('mon')
        else:
            u.mon = u.mon
            messages.warning(request, u'无法再次修改月')

        if not u.day:
            u.day = request.POST.get('day')
        else:
            u.day = u.day
            messages.warning(request, u'无法再次修改日')

        u.save()


    def frMt(self, request):
        from order.models import Ord

        try:
            request.user.newOrd = Ord.objects.lenNewOrd(request.user)
            request.user.newMsg = 0
            request.user.allMsg = request.user.newOrd + request.user.newMsg

        except Exception, e:
            pass


class BsInfo(models.Model):
    mons = (
                    (0, u'00'), 
                    (1, u'01'), 
                    (2, u'02'), 
                    (3, u'03'), 
                    (4, u'04'), 
                    (5, u'05'), 
                    (6, u'06'), 
                    (7, u'07'), 
                    (8, u'08'), 
                    (9, u'09'), 
                    (10, u'10'),  
                    (11, u'11'), 
                    (12, u'12'), 
                )
    days = (
                    (0, u'00'), 
                    (1, u'01'), 
                    (2, u'02'), 
                    (3, u'03'), 
                    (4, u'04'), 
                    (5, u'05'),
                    (6, u'06'), 
                    (7, u'07'), 
                    (8, u'08'), 
                    (9, u'09'), 
                    (10, u'10'), 
                    (11, u'11'), 
                    (12, u'12'), 
                    (13, u'13'), 
                    (14, u'14'), 
                    (15, u'15'),
                    (16, u'16'), 
                    (17, u'17'), 
                    (18, u'18'), 
                    (19, u'19'), 
                    (20, u'20'), 
                    (21, u'21'), 
                    (22, u'22'), 
                    (23, u'23'), 
                    (24, u'24'), 
                    (25, u'25'),
                    (26, u'26'), 
                    (27, u'27'), 
                    (28, u'28'), 
                    (29, u'29'), 
                    (30, u'30'), 
                    (31, u'31'), 
                )

    sexs =  (
                (0, u'保密'), 
                (1, u'先生'), 
                (2, u'女士'),
        )

    typs =  (
                (0, u'普通'), 
                (1, u'试吃'), 
        )

    user = models.OneToOneField(User, verbose_name=u'用户')
    mon = models.SmallIntegerField(u'月', default=0, choices=mons)
    day = models.SmallIntegerField(u'日', default=0, choices=days)
    sex = models.SmallIntegerField(u'性别', default=0, choices=sexs)
    typ = models.SmallIntegerField(u'类型', default=0, choices=typs)

    ure = ur'[1][3|4|5|8][0-9]\d{8}'

    objects = bsInfoManager()

    def __unicode__(self):
        return u"%s [ 性别：%s ] [ 生日：%s %s ]" % (self.user, self.get_sex_display(), self.get_mon_display(), self.get_day_display())

    def newUser(self, dic):

        u = User.objects.create_user(username=dic['username'], email=dic['email'], password='4000592731')
        try:
            u.first_name = dic['first_name']
            u.last_name = dic['last_name']
            u.is_active = True
            u.save()

            self.user = u

            self.mon = int(dic['mon'])

            self.day = int(dic['day'])

            self.sex = int(dic['sex'])
            self.typ = int(dic['typ'])
            self.save()

            p = Pts()

            p.pt = int(dic['pt']) if dic['pt'] else 0

            p.user = u

            p.save()
        except Exception, e:
            u.delete()
            # raise e

        return self

class Pts(models.Model):
    user = models.OneToOneField(User, verbose_name=u'用户')
    pt = models.IntegerField(u'积分', default=0)
        
    def __unicode__(self):
        return u"%s [ 积分:%s ]" % (self.user, self.pt)