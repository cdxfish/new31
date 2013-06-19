#coding:utf-8
from django import forms
from models import *
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


def getOTpyeForm(request):
    from views import Order

    return OrderTypeForm(initial= {'oType': Order(request).oType,})


class OrderTypeForm(forms.Form):

    oChoice = OrderInfo.oType

    oType = forms.ChoiceField(label=u'订单类型', choices=oChoice, widget=forms.Select(attrs={'class': 'oType' }))


class OrderStatusForm(forms.Form):

    oChoice = ((-1, '全部'),) + OrderInfo.oType
    cChoice = ((-1, '全部'),) + OrderStatus.oStatus

    o = forms.ChoiceField(label=u'订单类型', choices=oChoice, widget=forms.Select(attrs={'class': 'c' }))
    c = forms.ChoiceField(label=u'订单状态', choices=cChoice, widget=forms.Select(attrs={'class': 'o' }))
    s = forms.DateField(label="起始时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    e = forms.DateField(label="结束时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7},format='%Y-%m-%d'))
    k = forms.CharField(label=u'关键字', required=False)