#coding:utf-8
from django import forms
from purview.models import *
from models import *
from office.forms import *

# Create your forms here.

class ProduceForm(baseSearchForm):

    cChoice = ((-1, '全部'),) + Produce.oStatus
    c = forms.ChoiceField(label=u'生产状态', choices=cChoice, widget=forms.Select(attrs={'class': 'c' }))