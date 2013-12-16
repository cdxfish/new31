#coding:utf-8
from django import forms
# Create your forms here.

def payFrm(pay):

    PayFrm = type('PayFrm', (forms.Form, ), { i[0]:forms.CharField(label=u'%s' % i[1])for i in pay.main.config})

    return PayFrm(initial=dict({ i[0]:i[2] for i in pay.main.config }, **pay._config()))