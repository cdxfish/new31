#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from new31.decorator import timeit
# Create your models here.

class bsInfoManager(models.Manager):
    def set(self, request):

        u = request.user.userinfo

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

    # @timeit
    # def rUserd(self):
    #     u"""会员数据导入"""
    #     from models import uDATA, BsInfo, Pts
    #     from django.contrib.auth.models import User

    #     for i in uDATA.objects.all():
    #         try:
    #             u = User.objects.get(username=i.username)
    #             u.pts.pt = i.pt
    #             u.pts.save()

    #         except Exception, e:
    #             # raise e
    #             u = User.objects.create_user(username=i.username, email=i.email, password='4000592731')

    #             u.first_name = i.first_name
    #             u.last_name = i.last_name
    #             u.is_active = True
    #             u.save()
         
    #             b = BsInfo()
    #             b.user = u

    #             b.mon = i.mon

    #             b.day = i.day

    #             b.sex = i.sex
    #             b.typ = i.typ
    #             b.save()

    #             p = Pts()

    #             p.pt = i.pt

    #             p.user = u

    #             p.save()
    #         try:
    #             print '%06d - > %06d' % (i.id, u.id), u.username, '%02d-%02d' % (u.bsinfo.mon, u.bsinfo.day), u.pts.pt
    #         except Exception, e:
    #             # raise e
    #             u.delete()


class BsInfo(models.Model):
    mons = (
                    (0, u'保密'), 
                    (1, u'一月'), 
                    (2, u'二月'), 
                    (3, u'三月'), 
                    (4, u'四月'), 
                    (5, u'五月'), 
                    (6, u'六月'), 
                    (7, u'七月'), 
                    (8, u'八月'), 
                    (9, u'九月'), 
                    (10, u'十月'),  
                    (11, u'十一月'), 
                    (12, u'十二月'), 
                )
    days = (
                    (0, u'保密'), 
                    (1, u'一日'), 
                    (2, u'二日'), 
                    (3, u'三日'), 
                    (4, u'四日'), 
                    (5, u'五日'),
                    (6, u'六日'), 
                    (7, u'七日'), 
                    (8, u'八日'), 
                    (9, u'九日'), 
                    (10, u'十日'), 
                    (11, u'十一日'), 
                    (12, u'十二日'), 
                    (13, u'十三日'), 
                    (14, u'十四日'), 
                    (15, u'十五日'),
                    (16, u'十六日'), 
                    (17, u'十七日'), 
                    (18, u'十八日'), 
                    (19, u'十九日'), 
                    (20, u'二十日'), 
                    (21, u'二十一日'), 
                    (22, u'二十二日'), 
                    (23, u'二十三日'), 
                    (24, u'二十四日'), 
                    (25, u'二十五日'),
                    (26, u'二十六日'), 
                    (27, u'二十七日'), 
                    (28, u'二十八日'), 
                    (29, u'二十九日'), 
                    (30, u'三十日'), 
                    (31, u'三十一日'), 
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

# class uDATA(models.Model):
#     username = models.CharField(u'用户名', max_length=30, unique=True)
#     first_name = models.CharField(u'名', max_length=30, blank=True)
#     last_name = models.CharField(u'姓', max_length=30, blank=True)
#     email = models.EmailField(u'邮箱', blank=True)
#     mon = models.SmallIntegerField(u'月', default=0)
#     day = models.SmallIntegerField(u'日', default=0)
#     sex = models.SmallIntegerField(u'性别', default=0)
#     typ = models.SmallIntegerField(u'注册类型', default=0)
#     pt = models.IntegerField(u'积分', default=0)