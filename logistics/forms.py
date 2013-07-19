#coding:utf-8
from django import forms
from purview.models import *
from order.models import *
from office.forms import *

# Create your forms here.


class LogcsFrm(bsSrchFrm):

    chcs = ((-1, '全部'),) + OrdShip.chcs
    c = forms.ChoiceField(label=u'物流状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))



def AdvFrm(o):
    try:
        d = o.ordlogcs.dman.id
    except Exception, e:
        d = 0

    initial = {'advance': o.ordlogcs.advance, 'dman': d}

    class _AdvFrm(bsSrchFrm):
    	try:
    		dman = Role.objects.getDmanToTuple()
    	except Exception, e:
    		dman = ()

    	chcs = tuple([(0, u'物流师傅')] + list(dman))

        advance = forms.ChoiceField(label=u'提前量', choices=OrdLogcs.chcs, widget=forms.Select(attrs={'class': 'ad', 'id': 'a%s' %  o.sn }))
        dman = forms.ChoiceField(label=u'物流师傅', choices=chcs, widget=forms.Select(attrs={'class': 'dman', 'id': 'd%s' %  o.sn }))

    return _AdvFrm(initial=initial)
