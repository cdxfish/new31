#coding:utf-8
from django import forms
from purview.models import *
from order.models import *
from office.forms import *

# Create your forms here.


class LogcsForm(baseSearchForm):

    chcs = ((-1, '全部'),) + OrdShip.chcs
    c = forms.ChoiceField(label=u'物流状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))



def AdvanForm(o):
    initial = {'advance': o.ordlogcs.advance, 'dman': o.ordlogcs.dman}

    class AdvanceForm(baseSearchForm):

        advance = forms.ChoiceField(label=u'提前量', choices=OrdLogcs.chcs, widget=forms.Select(attrs={'class': 'ad', 'id': 'a%s' %  o.sn }))
        dman = forms.ChoiceField(label=u'物流师傅', choices=Role.objects.getDmanToTuple(), widget=forms.Select(attrs={'class': 'dman', 'id': 'd%s' %  o.sn }))

    return AdvanceForm(initial=initial)
