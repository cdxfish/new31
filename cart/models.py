#coding:utf-8
from django.db import models
from django.contrib.sessions.models import Session
from item.models import *
from shop.models import *

# Create your models here.

class Cart(models.Model):
    sessionKey = models.ForeignKey(Session)
    number = models.SmallIntegerField()
    itemAttr = models.ForeignKey(ItemAttr)
    type = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s - %s ( %s )" % (self.session_key, self.name, self.number, )