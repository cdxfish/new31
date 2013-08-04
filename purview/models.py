#coding:utf-8
from django.db import models

# Create your models here.

class roleManager(models.Manager):
    def getPath(self, path = ''):

        return self.select_related().get(path=path, onl=True)

    def getPathByUser(self, user):
        element = []
        role = self.select_related().filter(user=user, onl=True)

        for i in role:
            for ii in i.privilege.filter(onl=True):
                for iii in ii.element.filter(onl=True):
                    element.append(iii.path)

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
    from order.models import Ord
    from logistics.models import Logcs
    from produce.models import Pro
    from finance.models import Fnc
    from inventory.models import InvPro

    nPath = (
            (u'/', u'商城'),
            (u'/account/', u'用户中心'),
            (u'/account/login/', u'登录'),
            (u'/account/logout/', u'登出'),
            (u'/account/settings/', u'个人设置'),
            (u'/account/sset/', u'保存设置'),
            (u'/account/changepwd/', u'修改密码'),
            (u'/account/cpwd/', u'保存密码'),
            (u'/account/myord/', u'我的订单'),
            (u'/account/view/', u'订单详情'),
            (u'/cart/', u'购物车'),
            (u'/cart/del/', u'删除商品'),
        )


    pPath = (
                (u'/office/', U'管理中心'),
                (u'/order/', u'订单'),
                (u'/order/new/', u'新订单'),
                (u'/order/additemtoorder/', u'增订单商品'),
                (u'/order/delitem/', u'删订单商品'),
                (u'/order/edit/', u'编辑订单'),
                (u'/order/submit/', u'提交订单'),
            ) + \
            tuple([ (u'/order/%s/' % i, u'订单%s' % v) for i,v in Ord.chcs ]) + \
            (
                (u'/back/', u'退款'),
                (u'/logistics/', u'物流'),
                (u'/logistics/edit/', u'编辑物流'),
                (u'/logistics/submit/', u'提交物流'),
            ) + \
            tuple([ (u'/logistics/%s/' % i, u'物流%s' % v) for i,v in Logcs.chcs ]) + \
            (
                (u'/produce/', u'生产'),
            ) + \
            tuple([ (u'/produce/%s/' % i, u'生产%s' % v) for i,v in Pro.chcs ]) + \
            (
                (u'/inventory/', u'备货'), 
                (u'/inventory/list/', u'备货清单'), 
                (u'/inventory/conl/', u'备货选择'), 
                (u'/inventory/default/', u'备货格式化'), 
            ) + \
            tuple([ (u'/inventory/%s/' % i, u'备货%s' % v) for i,v in InvPro.typ ]) + \
            (
                (u'/after/', u'售后反馈'),
                (u'/tryeat/', u'试吃反馈'),
                (u'/applytryeat/', u'试吃'),
                (u'/discount/', u'会员折扣'),
                (u'/ticket/', u'蛋糕券'),
                (u'/integral/', u'积分换购'),
                (u'/party/', u'活动'),
                (u'/finance/', u'财务'),
            ) + \
            tuple([ (u'/finance/%s/' % i, u'财务%s' % v) for i,v in Fnc.chcs ]) + \
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
        if hasattr(self.sub, 'get_typ_display'):
            sub = self.sub.get_path_display()
        else:
            sub = None

        return u"%s [ %s ][ sub: %s ][ onl: %s ] - %s" % (self.get_path_display(), self.get_typ_display(), sub, self.onl, self.path)


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
    from django.contrib.auth.models import User
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