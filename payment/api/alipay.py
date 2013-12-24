#coding:utf-8
u"""支付宝"""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages, auth

def notify_url(request):
    u"""支付宝服务器异步通知页面路径"""

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))

def return_url(request):
    u"""支付宝页面跳转同步通知页面路径"""
    from payment.models import Pay
    from order.models import Ord

    get = request.GET.dict()

    o = Ord.objects.get(sn=get['out_trade_no'])

    messages.success(request, u'成功支付订单。')

    return redirect('account:uViewOrd', sn=201335702574608)

class Main(object):

    urls = (
            (r'^notify_url\/$', notify_url),
            (r'^return_url\/$', return_url),
        )


    conf = (
            ('partner', u'合作者身份ID', ''),
            ('key', u'支付宝私钥', ''),
            ('seller_email', u'卖家支付宝账号', ''),
            ('_input_charset', u'参数编码字符集', 'UTF-8'),
            ('sign_type', u'签名方式', u'MD5'),
            ('service', u'接口名称', u'create_direct_pay_by_user'),
            ('subject', u'交易标题', u'31客购物 订单编号: %s'),
            ('notify_url', u'服务器异步通知页面路径', u'http://www.31kecake.com/payment/api/alipay/notify_url/'),
            ('return_url', u'页面跳转同步通知页面路径 ', u'http://www.31kecake.com/payment/api/alipay/return_url/'),
            ('payment_type', u'支付类型', 1),
        )


    # 前台根据此方法返回的url地址生成支付按钮
    def postUrl(self):
        param = {
            'partner': self.partner,
            'seller_email': self.seller_email,
            '_input_charset': self._input_charset,
            'service': self.service,
            'notify_url': self.notify_url,
            'return_url': self.return_url,
            'out_trade_no': self.ord.sn,
            'subject': u'%s' % self.subject % self.ord.sn,
            'total_fee': self.ord.pro_set.all().total(),
            'payment_type': self.payment_type,
        }

        return u'https://mapi.alipay.com/gateway.do?' + \
         u'%s&sign=%s&sign_type=%s' % ( self.urlencode(param), self.sign(param), self.sign_type)

    def sign(self, dic):
        import hashlib

        s = u''
        for i in sorted(dic.items(), key=lambda x:x[0]):
            s += u'&%s=%s' % (i[0], i[1])

        m = hashlib.md5()
        m.update((s[1:] + self.key).encode(self._input_charset))

        return m.hexdigest()


    def urlencode(self, dic):
        import urllib

        _dic = dic.copy()

        for i in _dic:
            if type(_dic[i]) in (str, unicode):
                _dic[i] = _dic[i].encode(self._input_charset)

        return urllib.urlencode(_dic)