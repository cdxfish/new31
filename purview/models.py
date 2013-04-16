#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Element(models.Model):
    name = models.CharField(u'名称', max_length=32, unique=True)
    path = models.CharField(u'路径',max_length=60, unique=True)
    pType = models.SmallIntegerField(u'权限类型', choices=((1, u'查'), (2, u'增'), (3, u'删'), (4, u'改'), )) #权限类型共4种: {1:'查',2:'增',3:'删',4:'改',}
    onLine = models.BooleanField(u'上线', default=True)
    sub = models.ForeignKey("self",related_name='sub_set', verbose_name=u'从属', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ %s ][ sub: %s ][ onLine: %s ] - %s" % (self.name, self.get_pType_display(), self.sub, self.onLine, self.path)


class Privilege(models.Model):
    name = models.CharField(u'名称', max_length=32, unique=True)
    onLine = models.BooleanField(u'上线', default=True)
    element = models.ManyToManyField(Element, verbose_name=u'权限')

    def __unicode__(self):
        return u"%s [ onLine: %s ]" % (self.name, self.onLine)


class Role(models.Model):
    name = models.CharField(u'角色', max_length=32)
    onLine = models.BooleanField(u'上线', default=True)
    privilege = models.ForeignKey(Privilege, verbose_name=u'权限', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ onLine:%s ]" % (self.name, self.onLine)