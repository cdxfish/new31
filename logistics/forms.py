#coding:utf-8
from django import forms
from purview.models import *
from order.models import *
from office.forms import *

# Create your forms here.


class LogisticsForm(baseSearchForm):

    cChoice = ((-1, '全部'),) + OrdShip.chcs
    c = forms.ChoiceField(label=u'物流状态', choices=cChoice, widget=forms.Select(attrs={'class': 'c' }))



def AdvanForm(o):
    initial = {'advance': o.orderlogistics.advance, 'dman': o.orderlogistics.dman}

    class AdvanceForm(baseSearchForm):

        advance = forms.ChoiceField(label=u'提前量', choices=OrdLogcs.aChoice, widget=forms.Select(attrs={'class': 'ad', 'id': 'a%s' %  o.sn }))
        dman = forms.ChoiceField(label=u'物流师傅', choices=Role.objects.getDmanToTuple(), widget=forms.Select(attrs={'class': 'dman', 'id': 'd%s' %  o.sn }))

    return AdvanceForm(initial=initial)
