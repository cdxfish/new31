#coding:utf-8
from django import forms
from office.forms import bsSrchFrm

# Create your forms here.


class fncFrm(bsSrchFrm):
    from models import Fnc
    
    chcs = ((-1, '全部'),) + Fnc.chcs
    c = forms.ChoiceField(label=u'支付状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))