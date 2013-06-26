#coding:utf-8
from django import forms
from order.models import *
from signtime.models import *

# Create your forms here.


class baseSearchForm(forms.Form):

    oChoice = ((-1, '全部'),) + OrderInfo.oType

    o = forms.ChoiceField(label=u'订单类型', choices=oChoice, widget=forms.Select(attrs={'class': 'o' }))
    s = forms.DateField(label="起始时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    e = forms.DateField(label="结束时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    k = forms.CharField(label=u'关键字', required=False)