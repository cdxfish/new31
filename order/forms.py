#coding:utf-8
from django import forms
from models import *
from payment.models import *
from area.models import *
from signtime.models import *

# Create your forms here.

class ConsigneeForm(forms.ModelForm):

    pay = forms.ChoiceField(label=u'支付方式', choices=Pay.objects.getAll())
    time = forms.ChoiceField(label=u'最佳收货时间', choices=SignTime.objects.getAll())

    class Meta:
        model = OrderLogistics
        # exclude = ('order', 'logisDate', 'logisDate', 'logisTime', 'deliveryman',)
        fields = ('consignee', 'area', 'address', 'tel', 'signDate', 'note')
        widgets = {
            'address': forms.TextInput(attrs={'size': 70}),
            'tel': forms.TextInput(attrs={'size': 60}),
            'note': forms.Textarea(attrs={'cols': 100, 'rows': 4}),  
            'area': forms.Select(choices=Area.objects.getAll()),  
            'signDate': forms.DateInput(attrs={'class': 'date'}),  
        } 
