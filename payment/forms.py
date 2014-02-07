# coding: UTF-8
from django import forms
# Create your forms here.

def PayFrm(pay):

    return type('PayFrm', (forms.Form, ), { i[0]:forms.CharField(label=u'%s' % i[1]) for i in pay.main.conf})

def payFrm(pay):
    conf = pay._config()
    for i in conf.keys():
        if not conf[i]:
            del conf[i]

    return PayFrm(pay)(initial=dict({ i[0]:i[2] for i in pay.main.conf }, **conf))