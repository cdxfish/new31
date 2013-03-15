#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    birthMon = models.SmallIntegerField(u'出生月')
    birthDay = models.SmallIntegerField(u'出生日')
    sex = models.SmallIntegerField(u'性别')
    buycount = models.IntegerField(u'购买次数', default=0, editable=False)
    integral = models.IntegerField(u'积分', default=0, editable=False)
    regType = models.SmallIntegerField(u'注册类型', default=0, editable=False)
    regTime = models.DateTimeField(u'注册时间', auto_now=True, auto_now_add=True, editable=False)
    consignee = models.CharField(u'近期收货联系人', max_length=30)
    city = models.CharField(u'近期收货城市', max_length=32)
    block = models.CharField(u'近期收货区域', max_length=32)
    address = models.CharField(u'近期收货地址', max_length=120)
    tel = models.CharField(u'近期收货联系电话', max_length=60)
    date = models.DateField(u'近期收货日期')
    time = models.CharField(u'近期收货时间', max_length=30)

    def __unicode__(self):
        return u"%s" % self.user