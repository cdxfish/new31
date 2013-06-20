#coding:utf-8
from django import forms
from order.models import *

# Create your forms here.


class LogisticsForm(forms.Form):

    oChoice = ((-1, '全部'),) + OrderInfo.oType
    cChoice = ((-1, '全部'),) + OrderShip.sStatus

    o = forms.ChoiceField(label=u'订单类型', choices=oChoice, widget=forms.Select(attrs={'class': 'c' }))
    c = forms.ChoiceField(label=u'订单状态', choices=cChoice, widget=forms.Select(attrs={'class': 'c' }))
    s = forms.DateField(label="起始时间", widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    e = forms.DateField(label="结束时间", widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    k = forms.CharField(label=u'关键字', required=False)