#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey(User)
    birthmon = models.SmallIntegerField()
    birthday = models.SmallIntegerField()
    sex = models.SmallIntegerField()
    buycount = models.IntegerField()
    integral = models.IntegerField()
    regtype = models.SmallIntegerField()
    consignee = models.CharField(max_length=30)
    city = models.CharField(max_length=32)
    block = models.CharField(max_length=32)
    address = models.CharField(max_length=120)
    tel = models.CharField(max_length=60)
    date = models.DateField()
    time = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.user