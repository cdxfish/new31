# coding: UTF-8
from django import forms


# Create your forms here.

from office.forms import bsSrchFrm
class ProFrm(bsSrchFrm):
    from models import Pro

    chcs = ((-1, '全部'),) + Pro.chcs
    c = forms.ChoiceField(label=u'生产状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))