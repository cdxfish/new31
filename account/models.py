#coding:utf-8
from django.db import models

# Create your models here.

class User(models.Model):
    user = models.IntegerField()
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    birthmon = models.SmallIntegerField()
    birthday = models.SmallIntegerField()
    sex = models.SmallIntegerField()
    lastlogin = models.DateTimeField()
    lastip = models.IPAddressField()
    buycount = models.IntegerField()
    regtime = models.DateTimeField()
    type = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s" % self.user

class UserAddress(models.Model):
    user = models.OneToOneField(User)
    consignee = models.CharField(max_length=30)
    city = models.CharField(max_length=32)
    block = models.CharField(max_length=32)
    address = models.CharField(max_length=120)
    tel = models.CharField(max_length=60)
    date = models.DateField()
    time = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s - %s" % (self.consignee, self.address)
        
class UserBalance(models.Model):
    user = models.OneToOneField(User)
    integral = models.IntegerField()


    def __unicode__(self):
        return u"%s - %s" % (self.user, self.integral)