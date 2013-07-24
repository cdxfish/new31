#coding:utf-8
from django import forms
from office.forms import bsSrchFrm

# Create your forms here.


def ordForm(request):
    from views import OrdSess

    return OrdForm(initial= {'typ': int(OrdSess(request).o['typ']),})


class OrdForm(forms.Form):
    from models import Ord
    chcs = Ord.typs

    user = forms.CharField(label=u'会员帐号', required=False)
    typ = forms.ChoiceField(label=u'订单类型', choices=chcs, widget=forms.Select(attrs={'class': 'typ' }))


class OrdSrchFrm(bsSrchFrm):
    from models import Ord
    chcs = ((-1, '全部'),) + Ord.chcs

    c = forms.ChoiceField(label=u'订单状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))


class ItemsForm(object):

    @classmethod
    def getItemForms(self, items):

        for i in items:
            i.update({'forms': self._getItemForms(item=i)})

    @staticmethod
    def _getItemForms(item):
        from item.models import ItemSpec
        from discount.models import Dis

        mark = item['mark']
        speChcs = ItemSpec.objects.getTupleByItemID(item['item'].id)
        disChcs = Dis.objects.getTupleByAll()

        class orderItemForm(forms.Form):

            specID = forms.ChoiceField(label=u'规格', choices=speChcs, widget=forms.Select(attrs={'class': 'spec' , 'id':'s%d' % mark }))
            disID = forms.ChoiceField(label=u'折扣', choices=disChcs, widget=forms.Select(attrs={'class': 'dis', 'id':'d%d' % mark }))
            num = forms.IntegerField(label=u'数量', max_value=3, min_value=1, widget=forms.TextInput(attrs={'size': 1,'class': 'num', 'id':'n%d' % mark }))

        i = {'specID': item['spec'].id, 'disID': item['dis'].id, 'num': item['num']}

        return orderItemForm(initial= i)
