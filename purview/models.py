# coding: UTF-8
from django.core.urlresolvers import reverse
from django.db import models
import re

# Create your models here.

class roleManager(models.Manager):
    def getPath(self, path = ''):

        return self.select_related().get(path=path, onl=True)

    def getPathByUser(self, user):
        element = []
        role = self.select_related().filter(user=user, onl=True)

        if user.is_superuser:
            for i in Element.objects.filter(onl=True):
                element.append(i.path)

        else:

            for i in role:
                for ii in i.privilege.filter(onl=True):
                    for iii in ii.element.filter(onl=True):
                        element.append(iii.path)

        return element

    def getDmanToTuple(self):

        dMan = self.select_related().get(role=1,onl=True).user.filter(is_staff=True, is_active=True)

        return tuple([(i.id, u'%s%s' % (i.last_name, i.first_name) if (i.last_name or i.first_name) else i.username) for i in dMan])

    def getActByUser(self, user, act):

        return tuple( i for i in act if i[2] in self.getPathByUser(user))


    def getAjaxAct(self, l, sn):

        return tuple( ( i[0], i[1], i[2].replace(':',''), reverse(i[2], kwargs={'sn': sn, 's': i[0]}) ) for i in l )


class elementManager(models.Manager):
    def getPath(self, path = ''):

        return self.select_related().get(path=path, onl=True)

    def getDomElement(self):

        return self.select_related().filter(onl=True)


    def getUserByPath(self, path):
        from django.core.urlresolvers import resolve
        users = []
        for i in self.select_related().get(path=resolve(path).view_name).privilege_set.all():
            for ii in i.role_set.all():
                for iii in ii.user.all():
                    if not iii in users:
                        users.append(iii)

        return users


class Element(models.Model):
    from django.conf import settings
    from new31.func import Patterns, resolves

    paths = resolves(Patterns(settings.APPS.keys()))
    nPath = tuple(paths[0])
    pPath = tuple(paths[1])

    path = models.CharField(u'路径',max_length=255, choices=tuple((i[0],i[1]) for i in pPath), unique=True)
    onl = models.BooleanField(u'上线', default=True)

    objects = elementManager()

    def __unicode__(self):

        return u"%s [ onl: %s ] - %s" % (self.get_path_display(), self.onl, self.path)

    class Meta:
        ordering = ['-path']
        verbose_name_plural = u'页面'
        # app_label = 'auth'


class EleSub(models.Model):
    path = models.ForeignKey(Element, verbose_name=u'路径')
    sub = models.ForeignKey(Element, verbose_name=u'从属', related_name='sub')

    def __unicode__(self):

        return u"%s -> %s" % (self.path.get_path_display(), self.sub.get_path_display())

    class Meta:
        ordering = ['-path']
        verbose_name_plural = u'从属'
        # app_label = 'auth'


class Privilege(models.Model):
    chcs = (
            (0, u'技术部'),
            (1, u'物流部'),
            (2, u'后勤部A'),
            (3, u'客服部A'),
            (4, u'业务部A'),
            (5, u'生产部A'),
            (6, u'财务部A'),
            (7, u'客服部B'),
            (8, u'业务部B'),
            (9, u'生产部B'),
            (10, u'财务部B'),
        )
    name = models.SmallIntegerField(u'名称', choices=chcs, unique=True)
    onl = models.BooleanField(u'上线', default=True)
    element = models.ManyToManyField(Element, verbose_name=u'权限', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ onl: %s ]" % (self.get_name_display(), self.onl)

    class Meta:
        verbose_name_plural = u'权限集'
        # app_label = 'auth'


class Role(models.Model):
    from django.contrib.auth.models import User
    chcs = (
            (-1, u'管理员'),
            (0, u'无'),
            (1, u'物流师傅'),
            (2, u'调度'),
            (3, u'业务'),
            (4, u'业务主管'),
            (5, u'业务经理'),
            (6, u'市场总监'),
            (7, u'客服'),
            (8, u'行政客服'),
            (9, u'客服主管'),
            (10, u'客服经理'),
            (11, u'生产'),
            (12, u'总经理'),
            (13, u'副经理'),
            (14, u'会计'),
            (15, u'出纳'),
            (16, u'现场主管'),
        )

    role = models.SmallIntegerField(u'角色', choices=chcs, unique=True)
    user = models.ManyToManyField(User, verbose_name=u'用户', blank=True, null=True)
    privilege = models.ManyToManyField(Privilege, verbose_name=u'权限', blank=True, null=True)
    onl = models.BooleanField(u'上线', default=True)

    objects = roleManager()

    def __unicode__(self):
        return u"%s [ onl:%s ]" % (self.get_role_display(), self.onl)

    class Meta:
        verbose_name_plural = u'角色'
        # app_label = 'auth'