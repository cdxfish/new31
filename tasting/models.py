# coding: UTF-8
from django.db import models

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
    address = models.CharField(u'公司地址', max_length=60)
    department = models.CharField(u'公司部门', max_length=60)
    contact = models.CharField(u'联系人', max_length=60)
    tel = models.CharField(u'联系电话', max_length=60)
    time = models.SmallIntegerField(u'时间安排', default=0, choices=chcs)
    scale = models.SmallIntegerField(u'公司规模', default=0, choices=_chcs)
    addtime = models.DateTimeField(u'申请时间', auto_now=True, auto_now_add=True, editable=False)


    def __unicode__(self):
        return u"%s - %s" % (self.company, self.addtime)

    class Meta:
        ordering = ['addtime']
        verbose_name_plural = u'试吃申请'