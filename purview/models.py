#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Element(models.Model):
    pPath = (
          (u'/office/', U'管理中心'),
          (u'/order/', u'订单'),
          (u'/order/new/', u'新订单'),
          (u'/order/e/', u'订单修改'),
          (u'/order/add/', u'增订单'),
          (u'/order/edit/', u'改订单'),
          (u'/order/del/', u'删订单'),
          (u'/back/', u'退款'),
          (u'/logistics/', u'物流管理'),
          (u'/produce/', u'生产管理'),
          (u'/inventory/', u'库存'),
          (u'/after/', u'售后反馈'),
          (u'/tryeat/', u'试吃反馈'),
          (u'/applytryeat/', u'试吃'),
          (u'/discount/', u'会员折扣'),
          (u'/ticket/', u'蛋糕券'),
          (u'/integral/', u'积分换购'),
          (u'/party/', u'活动'),
          (u'/reconciliation/', u'订单对账'),
          (u'/approved/', u'账单核准'),
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
          (u'/area/', u'配送区域'),
          (u'/filecheck/', u'文件校验'),
        ) #权限对照用列表,用于识别那些页面需要进行权限判定

    path = models.CharField(u'路径',max_length=255, choices=pPath)
    #权限类型共4种: {0:'查',1:'显',2:'增',3:'删',4:'改',} 其中显为界面显示专属
    pType = models.SmallIntegerField(u'权限类型',default=0, choices=((0, u'查 (无从属)'), (1, u'显'), (2, u'增'), (3, u'删'), (4, u'改'), )) 
    onLine = models.BooleanField(u'上线', default=True)
    sub = models.ForeignKey("self",related_name='sub_set', verbose_name=u'从属', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ %s ][ sub: %s ][ onLine: %s ] - %s" % (self.get_path_display(), self.get_pType_display(), self.sub, self.onLine, self.path)


class Privilege(models.Model):
    name = models.CharField(u'名称', max_length=32, unique=True)
    onLine = models.BooleanField(u'上线', default=True)
    element = models.ManyToManyField(Element, verbose_name=u'权限', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ onLine: %s ]" % (self.name, self.onLine)


class Role(models.Model):
    name = models.CharField(u'角色', max_length=32)
    onLine = models.BooleanField(u'上线', default=True)
    privilege = models.ForeignKey(Privilege, verbose_name=u'权限', blank=True, null=True)

    def __unicode__(self):
        return u"%s [ onLine:%s ]" % (self.name, self.onLine)