#coding:utf-8
from django import forms
from order.models import *
from payment.models import *
from area.models import *
from signtime.models import *

# Create your forms here.

class ConsigneeForm(forms.ModelForm):
    user = forms.CharField(label=u'会员帐号', required=False)
    pay = forms.ChoiceField(label=u'支付方式', choices=Pay.objects.getTupleByAll())
    time = forms.ChoiceField(label=u'收货时间', choices=SignTime.objects.getTupleByAll())

    class Meta:
        model = OrdLogcs
        fields = ('consignee', 'area', 'address', 'tel', 'signDate', 'note')
        widgets = {
            'address': forms.TextInput(attrs={'size': 70}),
            'tel': forms.TextInput(attrs={'size': 60}),
            'note': forms.Textarea(attrs={'cols': 100, 'rows': 4}),  
            'area': forms.Select(choices=Area.objects.getTupleByAll()),  
            'signDate': forms.DateInput(attrs={'class': 'date'},format='%Y-%m-%d'),  
        }


def getForms(request):

    consignee = {i:v for i, v in request.session['c'].items()}

    return ConsigneeForm(initial= consignee)