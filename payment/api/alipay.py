#coding:utf-8
u"""支付宝"""

class Main(object):
    urls = ()

    config = (
            ('partner', u'合作者身份ID', ''),
            ('_input_charset', u'参数编码字符集', 'UTF-8'),
            ('sign_type', u'签名方式', 'MD5'),
            ('service', u'接口名称', 'create_direct_pay_by_user'),
        )


    # 前台根据此方法返回的url地址生成支付按钮
    def button(self):

        return 'https://mapi.alipay.com/gateway.do?'