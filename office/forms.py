#coding:utf-8
from django import forms
from order.models import *
from signtime.models import *

# Create your forms here.


class bsSrchFrm(forms.Form):

    chcs = ((-1, '全部'),) + Ord.typs

    o = forms.ChoiceField(label=u'订单类型', choices=chcs, widget=forms.Select(attrs={'class': 'o' }))
    c = forms.ChoiceField(label=u'c', choices=chcs, widget=forms.Select(attrs={'class': 'c' })) 
    s = forms.DateField(label="起始时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    e = forms.DateField(label="结束时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    k = forms.CharField(label=u'关键字', required=False)