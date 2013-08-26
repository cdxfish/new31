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

    chcs = ((0, u'json'), (1, u'查'), (2, u'增'), (3, u'删'), (4, u'改'), )

    pPath = (
                (u'/office/', u'管理中心', 1),
                (u'/order/', u'订单', 1),
                (u'/order/view/', u'查询订单', 1),
                (u'/order/print/', u'打印订单', 1),
                (u'/order/new/', u'新订单', 1),
                (u'/order/additemtoorder/', u'增订单商品', 2),
                (u'/order/delitem/', u'删订单商品', 3),
                (u'/order/edit/', u'编辑订单', 4),
                (u'/order/submit/', u'提交订单', 2),
            ) + \
            tuple([ (u'/order/%s/' % i, u'订单%s' % v, 4) for i,v in Ord.chcs ]) + \
            (
                (u'/back/', u'退款', 4),
                (u'/logistics/', u'物流', 1),
                (u'/logistics/map/', u'地图', 1),
                (u'/logistics/view/', u'物流安排', 1),
                (u'/logistics/edit/', u'编辑物流', 1),
                (u'/logistics/submit/', u'提交物流', 1),
            ) + \
            tuple([ (u'/logistics/%s/' % i, u'物流%s' % v, 4) for i,v in Logcs.chcs ]) + \
            (
                (u'/produce/', u'生产', 1),
            ) + \
            tuple([ (u'/produce/%s/' % i, u'生产%s' % v, 4) for i,v in Pro.chcs ]) + \
            (
                (u'/inventory/', u'备货', 1), 
                (u'/inventory/list/', u'备货清单', 1), 
                (u'/inventory/conl/', u'备货选择', 1), 
                (u'/inventory/default/', u'备货格式化', 1), 
            ) + \
            tuple([ (u'/inventory/%s/' % i, u'备货%s' % v, 4) for i,v in InvPro.typ ]) + \
            (
                (u'/after/', u'售后反馈', 1),
                (u'/tryeat/', u'试吃反馈', 1),
                (u'/applytryeat/', u'试吃', 1),
                (u'/discount/', u'会员折扣', 1),
                (u'/ticket/', u'蛋糕券', 1),
                (u'/integral/', u'积分换购', 1),
                (u'/party/', u'活动', 1),
                (u'/finance/', u'财务', 1),
            ) + \
            tuple([ (u'/finance/%s/' % i, u'财务%s' % v, 4) for i,v in Fnc.chcs ]) + \
            (
                (u'/reimburse/', u'退款', 1),
                (u'/statistics/', u'订单统计', 1),
                (u'/statssale/', u'销售明细', 1),
                (u'/member/', u'会员信息', 1),
                (u'/memberint/', u'会员积分', 1),
                (u'/purview/', u'权限分配', 1),
                (u'/adminlog/', u'管理员日志', 1),
                (u'/system/', u'系统设置', 1),
                (u'/item/item/', u'商品', 1),
                (u'/tag/tag/', u'标签', 1),
                (u'/spec/', u'规格', 1),
                (u'/price/', u'价格', 1),
                (u'/slide/', u'首页幻灯片', 1),
                (u'/payment/', u'支付方式', 1),
                (u'/signtime/', u'收货时间', 1),
                (u'/logistics/time/', u'物流时间', 1),
                (u'/bom/', u'物料', 1),
                (u'/area/', u'配送区域', 1),
                (u'/filecheck/', u'文件校验', 1),
                (u'/ajax/user/', u'ajax 会员查询', 0),
                (u'/ajax/cord/', u'ajax 修改订单信息', 0),
                (u'/ajax/cdman/', u'ajax 修改物流师傅', 0),
                (u'/ajax/cadv/', u'ajax 修改物流偏移量', 0),
                (u'/ajax/item/', u'ajax 商品查询', 0),
            )
        #权限对照用列表,用于识别那些页面需要进行权限判定


    nPath = (
            (u'/', u'商城'),
            (u'/admin/', u'站点管理'),
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
            (u'/cart/buy/', u'购买商品'),
            (u'/cart/del/', u'删除商品'),
            (u'/cart/consignee/', u'收货人信息'),
            (u'/tag/', u'标签'),
        )

    path = models.CharField(u'路径',max_length=255, choices=tuple([(i[0],i[1]) for i in pPath]), unique=True)
    #权限类型共4种: {0:'查',1:'显',2:'增',3:'删',4:'改',} 其中显为界面显示专属
    # typ = models.SmallIntegerField(u'权限类型',default=0, choices=chcs)
    onl = models.BooleanField(u'上线', default=True)
    sub = models.ForeignKey("self",related_name='sub_set', verbose_name=u'从属', blank=True, null=True)

    objects = elementManager()

    def __unicode__(self):
        if hasattr(self.sub, 'get_typ_display'):
            sub = self.sub.get_path_display()
        else:
            sub = None

        return u"%s [ sub: %s ][ onl: %s ] - %s" % (self.get_path_display(), sub, self.onl, self.path)


class Privilege(models.Model):
    chcs = (
            (0, u'技术部'),
            (1, u'物流部'),
            (2, u'后勤部'),
            (3, u'客服部'),
            (4, u'业务部'),
            (5, u'生产部'),
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
        )

    role = models.SmallIntegerField(u'角色', choices=chcs, unique=True)
    user = models.ManyToManyField(User, verbose_name=u'用户', blank=True, null=True)
    privilege = models.ManyToManyField(Privilege, verbose_name=u'权限', blank=True, null=True)
    onl = models.BooleanField(u'上线', default=True)

    objects = roleManager()

    def __unicode__(self):
        return u"%s [ onl:%s ]" % (self.get_role_display(), self.onl)