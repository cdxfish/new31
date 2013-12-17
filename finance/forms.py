#coding:utf-8
from django import forms
from office.forms import bsSrchFrm

# Create your forms here.

def FncFrm(request):
    from payment.models import Pay

    if request.user.is_staff:
        pay = forms.ChoiceField(label=u'支付方式', choices=Pay.objects.getTpl(), required=False)

    else:

        pay = forms.ChoiceField(label=u'支付方式', choices=Pay.objects.getTplToShow(), required=False)

    return type('_FncFrm', (forms.Form,), {'pay': pay})

def fncFrm(request):
    from views import FncSess

    return FncFrm(request)(initial=FncSess(request).sess)

class FncSrchFrm(bsSrchFrm):
    from models import Fnc
    
    chcs = ((-1, '全部'),) + Fnc.chcs
    c = forms.ChoiceField(label=u'支付状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))