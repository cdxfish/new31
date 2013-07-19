#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from order.models import *
from produce.models import *

# Create your models here.

class roleManager(models.Manager):
    def getPath(self, path = ''):

        return self.select_related().get(path=path, onl=True)

    def getPathByUser(self, user):
        element = []
        role = self.select_related().get(user=user, onl=True)

        for i in role.privilege.filter(onl=True):
            for ii in i.element.filter(onl=True):
                element.append(ii.path)

        return element

    def getDmanToTuple(self):

        dMan = self.select_related().get(role=1,onl=True).user.all()

        return tuple([(i.id, u'%s%s' % (i.last_name, i.first_name) if (i.last_name or i.first_name) else i.username) for i in dMan])

class elementManager(models.Manager):
    def getPath(self, path = ''):

        return self.select_related().get(path=path, onl=True)

    def getDomElement(self):

        return self.select_related().filter(onl=True)


class Element(models.Model):
    pPath = (
                (u'/office/', U'管理中心'),
                (u'/order/', u'订单'),
            ) + \
            tuple([ (u'/order/%s/' % i, u'订单%s' % v) for i,v in OrdStatus.chcs ]) + \
            (
                (u'/order/new/', u'新订单'),
                (u'/order/edit/', u'编辑订单'),
                (u'/order/submit/', u'提交订单'),
                (u'/back/', u'退款'),
                (u'/logistics/', u'物流'),
            ) + \
            tuple([ (u'/logistics/%s/' % i, u'物流%s' % v) for i,v in OrdShip.chcs ]) + \
            (
                (u'/produce/', u'生产'),
            ) + \
            tuple([ (u'/produce/%s/' % i, u'生产%s' % v) for i,v in Produce.chcs ]) + \
            (
                (u'/inventory/', u'备货'),
                (u'/after/', u'售后反馈'),
                (u'/tryeat/', u'试吃反馈'),
                (u'/applytryeat/', u'试吃'),
                (u'/discount/', u'会员折扣'),
                (u'/ticket/', u'蛋糕券'),
                (u'/integral/', u'积分换购'),
                (u'/party/', u'活动'),
                (u'/finance/', u'财务'),
            ) + \
            tuple([ (u'/finance/%s/' % i, u'财务%s' % v) for i,v in OrdPay.chcs ]) + \
            (
                (u'/reimburse/', u'退款'),
                (u'/statistics/', u'订单统计'),
                (u'/statssale/', u'销售明细'),
                (u'/member/', u'会员信息'),
                (u'/memberint/', u'会员积分'),
                (u'/purview/', u'权限分配'),
                (u'/adminlog/', u'管理员日志'),
                (u'/system/', u'系统设置'),
                (u'/item/item/', u'商品'),
                (u'/tag/tag/', u'标签'),
                (u'/spec/', u'规格'),
                (u'/price/', u'价格'),
                (u'/slide/', u'首页幻灯片'),
                (u'/payment/', u'支付方式'),
                (u'/signtime/', u'收货时间'),
                (u'/logistics/time/', u'物流时间'),
                (u'/bom/', u'物料'),
                (u'/area/', u'配送区域'),
                (u'/filecheck/', u'文件校验'),
                (u'/map/', u'地图'),
            )
         #权限对照用列表,用于识别那些页面需要进行权限判定

    chcs = ((0, u'json'), (1, u'查'), (2, u'增'), (3, u'删'), (4, u'改'), )

    path = models.CharField(u'路径',max_length=255, choices=pPath, unique=True)
    #权限类型共4种: {0:'查',1:'显',2:'增',3:'删',4:'改',} 其中显为界面显示专属
    typ = models.SmallIntegerField(u'权限类型',default=0, choices=chcs)
    onl = models.BooleanField(u'上线', default=True)
    sub = models.ForeignKey("self",related_name='sub_set', verbose_name=u'从属', blank=True, null=True)

    objects = elementManager()

    def __unicode__(self):
        return u"%s [ %s ][ sub: %s ][ onl: %s ] - %s" % (self.get_path_display(), self.get_typ_display(), self.sub, self.onl, self.path)


class Privilege(models.Model):
    chcs = (
            (0, u'全局可读可写'),
        )
    name = models.SmallIntegerField(u'名称', choices=chcs, unique=True)
    onl = models.BooleanField(u'上线', default=True)
    element = models.ManyToManyField(Element, verbose_name=u'权限', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ onl: %s ]" % (self.get_name_display(), self.onl)


class Role(models.Model):
    chcs = (
            (-1, u'管理员'),
            (0, u'无'),
            (1, u'物流师傅'),
        )

    role = models.SmallIntegerField(u'角色', choices=chcs, unique=True)
    user = models.ManyToManyField(User, verbose_name=u'用户', blank=True, null=True)
    onl = models.BooleanField(u'上线', default=True)
    privilege = models.ManyToManyField(Privilege, verbose_name=u'权限', blank=True, null=True)

    objects = roleManager()

    def __unicode__(self):
        return u"%s [ onl:%s ]" % (self.get_role_display(), self.onl)