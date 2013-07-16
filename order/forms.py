#coding:utf-8
from django import forms
from office.forms import *
from models import *
from payment.models import *
from area.models import *
from signtime.models import *

# Create your forms here.


def getOTpyeForm(request):
    from views import Order

    return OrderTypeForm(initial= {'oType': int(Order(request).o['typ']),})


class OrderTypeForm(forms.Form):

    chcs = OrderInfo.chcs

    oType = forms.ChoiceField(label=u'订单类型', choices=chcs, widget=forms.Select(attrs={'class': 'oType' }))


class OrderStatusForm(baseSearchForm):

    chcs = ((-1, '全部'),) + OrderStatus.chcs

    c = forms.ChoiceField(label=u'订单状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))


class ItemsForm(object):

    @classmethod
    def getItemForms(self, items):

        for i in items:
            i.update({'forms': self._getItemForms(item=i)})

    @staticmethod
    def _getItemForms(item):
        mark = item['mark']
        speChcs = ItemSpec.objects.getTupleByItemID(item['item'].id)
        disChcs = Discount.objects.getTupleByAll()

        class orderItemForm(forms.Form):

            specID = forms.ChoiceField(label=u'规格', choices=speChcs, widget=forms.Select(attrs={'class': 'spec' , 'id':'s%d' % mark }))
            disID = forms.ChoiceField(label=u'折扣', choices=disChcs, widget=forms.Select(attrs={'class': 'dis', 'id':'d%d' % mark }))
            num = forms.IntegerField(label=u'数量', max_value=3, min_value=1, widget=forms.TextInput(attrs={'size': 1,'class': 'num', 'id':'n%d' % mark }))

        i = {'specID': item['spec'].id, 'disID': item['dis'].id, 'num': item['num']}

        return orderItemForm(initial= i)
