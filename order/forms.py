#coding:utf-8
from django import forms
from order.models import *
from payment.models import *
from area.models import *
from signtime.models import *

# Create your forms here.

def getItemForms(item):
    mark = item['mark']
    speChoice = ItemSpec.objects.getTupleByItemID(item['item'].id)
    disChoice = Discount.objects.getTupleByAll()

    class orderItemForm(forms.Form):

        specID = forms.ChoiceField(label=u'规格', choices=speChoice, widget=forms.Select(attrs={'class': 'spec' , 'id':'s%d' % mark }))
        disID = forms.ChoiceField(label=u'折扣', choices=disChoice, widget=forms.Select(attrs={'class': 'dis', 'id':'d%d' % mark }))
        num = forms.IntegerField(label=u'数量', max_value=3, min_value=1, widget=forms.TextInput(attrs={'size': 1,'class': 'num', 'id':'n%d' % mark }))

    i = {'specID': item['spec'].id, 'disID': item['dis'].id, 'num': item['num']}

    return orderItemForm(initial= i)



def getForms(request):

    consignee = {i:v for i, v in request.session['c'].items()}

    return ConsigneeForm(initial= consignee)
