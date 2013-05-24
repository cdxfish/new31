#coding:utf-8
from django import forms
from order.models import *
from payment.models import *
from area.models import *
from signtime.models import *

# Create your forms here.

def getItemForms(item):
    mark = item['mark']
    itemSpecs = ItemSpec.objects.getSpecByItemID(item['item'].id)
    itemFees = ItemFee.objects.getFeeBySpecID(item['spec'].id)

    speChoice = ((i.spec.id, i.spec.value) for i in  itemSpecs)
    disChoice = ((i.itemdiscount.discount.id, i.itemdiscount.discount.get_discount_display()) for i in  itemFees)


    class orderItemForm(forms.Form):

        spec = forms.ChoiceField(label=u'规格', choices=speChoice, widget=forms.Select(attrs={'class': 's%d' % mark,'id':'s%d' % mark }))
        dis = forms.ChoiceField(label=u'折扣', choices=disChoice, widget=forms.Select(attrs={'class': 'd%d' % mark,'id':'d%d' % mark }))
        num = forms.IntegerField(label=u'数量', max_value=3, min_value=1, widget=forms.TextInput(attrs={'size': 1,'class': 'n%d' % mark,'id':'n%d' % mark }))

    i = {'spec': item['spec'].id, 'dis': item['dis'].id, 'num': item['num']}

    return orderItemForm(initial= i)



def getForms(request):

    consignee = {i:v for i, v in request.session['c'].items()}

    return ConsigneeForm(initial= consignee)
