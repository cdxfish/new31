#coding:utf-8
from django import forms
from order.models import *
from office.forms import *

# Create your forms here.


class financeForm(baseSearchForm):

    cChoice = ((-1, '全部'),) + OrderPay.chcs
    c = forms.ChoiceField(label=u'支付状态', choices=cChoice, widget=forms.Select(attrs={'class': 'c' }))