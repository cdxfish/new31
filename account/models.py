#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from purview.models import *

# Create your models here.

class UserInfo(models.Model):
    mons = (
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
                (u'M', u'先生'), 
                (u'F', u'女士'),
        )

    user = models.OneToOneField(User, verbose_name=u'用户')
    birthMon = models.SmallIntegerField(u'出生月', choices=mons)
    birthDay = models.SmallIntegerField(u'出生日', choices=days)
    sex = models.CharField(u'性别',max_length=1, choices=sexs)
    typ = models.SmallIntegerField(u'注册类型', default=0, editable=False)

    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.user, self.regTime)