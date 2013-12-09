#coding:utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class AreaManager(models.Manager):
    def getAreaById(self, id = ''):

        return self.select_related().get(onl=True, id=id)

    def default(self):

        return self.select_related().filter(onl=True)[0].sub_set.filter(onl=True)[0]

    def getTpl(self):

        return tuple((i.id, '%s' % i.get_name_display()) for i in self.filter(onl=True) )

class AttributionManager(models.Manager):
    def getAreaName(self):

        return [ i.area.get_name_display() for i in self.all()]

class Area(models.Model):
    chcs = (
            (0, u'南宁 - 青秀区'),
            (1, u'南宁 - 江南区'),
            (2, u'南宁 - 兴宁区'),
            (3, u'南宁 - 邕宁区'),
            (4, u'南宁 - 良庆区'),
            (5, u'南宁 - 西乡塘区'),
            (6, u'长沙 - 芙蓉区'),
            (7, u'长沙 - 天心区'),
            (8, u'长沙 - 岳麓区'),
            (9, u'长沙 - 开福区'),
            (10, u'长沙 - 雨花区'),
            (11, u'长沙 - 望城区'),
            (12, u'长沙 - 长沙县'),
        )
    name = models.SmallIntegerField(u'区域', unique=True, default=0, choices=chcs)
    onl = models.BooleanField(u'上线', default=True)

    objects = AreaManager()

    def __unicode__(self):
        return u"%s [ onl: %s]" % (self.get_name_display(), self.onl)

class Attribution(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    area = models.ForeignKey(Area, verbose_name=u'地区')

    objects = AttributionManager()

    def __unicode__(self):
        return u"%s [ %s ]" % (self.user, self.area.get_name_display())

    class Meta:
        ordering = ['user']
        unique_together=(('user', 'area'),)