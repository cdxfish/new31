#coding:utf-8
from django import forms
from order.models import *
from payment.models import *
from area.models import *
from signtime.models import *

# Create your forms here.

class orderItemForm(forms.ModelForm):

    spec = forms.ChoiceField(label=u'规格', choices=Pay.objects.getTupleByAll())
    dis = forms.ChoiceField(label=u'折扣', choices=Pay.objects.getTupleByAll())
    num = forms.IntegerField(label=u'数量', max_value=255, min_value=1)


def getForms(request):

    consignee = {i:v for i, v in request.session['c'].items()}

    return ConsigneeForm(initial= consignee)