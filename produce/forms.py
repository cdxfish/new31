#coding:utf-8
from django import forms
from purview.models import *
from models import *
from office.forms import *

# Create your forms here.

class ProFrm(bsSrchFrm):

    chcs = ((-1, '全部'),) + Pro.chcs
    c = forms.ChoiceField(label=u'生产状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))