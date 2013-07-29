#coding:utf-8
from django import forms
from office.forms import bsSrchFrm

# Create your forms here.

class FncFrm(forms.Form):
    from payment.models import Pay

    pay = forms.ChoiceField(label=u'支付方式', choices=Pay.objects.getTpl())


def fncFrm(request):
    from views import FncSess

    return FncFrm(initial={i:v for i, v in FncSess(request).sess.items()})

class FncSrchFrm(bsSrchFrm):
    from models import Fnc
    
    chcs = ((-1, '全部'),) + Fnc.chcs
    c = forms.ChoiceField(label=u'支付状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))