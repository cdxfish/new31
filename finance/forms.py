#coding:utf-8
from django import forms
from order.models import *
from office.forms import *

# Create your forms here.


class financeForm(bsSrchFrm):

    chcs = ((-1, '全部'),) + OrdPay.chcs
    c = forms.ChoiceField(label=u'支付状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))