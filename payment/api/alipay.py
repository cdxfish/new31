#coding:utf-8
u"""支付宝"""
from django.shortcuts import render_to_response
from django.template import RequestContext

class Main(object):
    def notify_url(request):
        u"""支付宝服务器异步通知页面路径"""

        return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))

    def return_url(request):
        u"""支付宝页面跳转同步通知页面路径"""

        return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))

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
        from django.utils.http import urlquote

        param = self.join({
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
        })

        return u'https://mapi.alipay.com/gateway.do?' + \
         u'%s&sign=%s&sign_type=%s' % ( param, self.sign(param + self.key), self.sign_type)

    def sign(self, s):
        import hashlib
        m = hashlib.md5()
        m.update(s.encode(self._input_charset))

        return m.hexdigest()

    def join(self, dic, reverse=False):
        param = ''
        print sorted(dic.items(), key=lambda x:x[0])
        for i in sorted(dic.items(), key=lambda x:x[0], reverse=reverse):
            param += '&%s=%s' % (i[0], i[1])

        return param[1:]