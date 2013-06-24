#coding:utf-8
from django import forms
from order.models import *
from office.forms import *

# Create your forms here.


class LogisticsForm(baseSearchForm):

    cChoice = ((-1, '全部'),) + OrderShip.oStatus
    c = forms.ChoiceField(label=u'物流状态', choices=cChoice, widget=forms.Select(attrs={'class': 'c' }))