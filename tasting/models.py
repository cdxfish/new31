# coding: UTF-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Apply(models.Model):
    chcs = (
            (0, u'上午'),
            (1, u'下午'),
        )

    _chcs = (
            (0, u'10 - 50'),
            (1, u'50 - 100'),
            (2, u'100 - 500'),
            (3, u'500 - 1000'),
            (4, u'1000 +'),
        )

    company = models.CharField(u'公司名称', max_length=30)
    area = models.CharField(u'公司所在区域', max_length=60)
    address = models.CharField(u'公司地址', max_length=60)
    department = models.CharField(u'公司部门', max_length=60)
    applicant = models.CharField(u'联系人', max_length=60)
    tel = models.CharField(u'联系电话', max_length=60)
    phone = models.CharField(u'办公电话', max_length=60)
    time = models.SmallIntegerField(u'时间安排', default=0, choices=chcs)
    scale = models.SmallIntegerField(u'公司规模', default=0, choices=_chcs)
    addtime = models.DateTimeField(u'申请时间', auto_now=True, auto_now_add=True, editable=False)


    def __unicode__(self):
        return u"%s - %s" % (self.company, self.addtime)

    class Meta:
        ordering = ['addtime']
        verbose_name_plural = u'试吃申请'


class ApplyArea(models.Model):
    from area.models import Area

    area = models.OneToOneField(Area, verbose_name=u'区域')
    onl = models.BooleanField(u'上线', default=True)


    def __unicode__(self):
        return u"%s - [%s]" % (self.area.get_name_display(), self.onl)

    class Meta:
        ordering = ['area']
        verbose_name_plural = u'申请开放区域'


class Discuss(models.Model):
    _chcs = (
                (0, u'未谈', 'tasting:copyOrd'),
                (1, u'接洽', 'tasting:editOrd'),
                (2, u'拒谈', 'tasting:confirmOrd'),
                # (3, u'无效', 'tasting:nullOrd'),
                # (4, u'止单', 'tasting:stopOrd'),
            )
    chcs= tuple((i[0], i[1]) for i in _chcs)


    app = models.OneToOneField(Apply, verbose_name=u'试吃申请')
    user = models.ForeignKey(User, verbose_name=u'管理员', blank=True, null=True)
    status = models.SmallIntegerField(u'洽谈状态', default=0, choices=chcs)
    note = models.CharField(u'备注', max_length=60)


    def __unicode__(self):
        return u"%s - [%s]" % (self.app.company, self.get_status_display())

    class Meta:
        ordering = ['app']
        verbose_name_plural = u'洽谈'