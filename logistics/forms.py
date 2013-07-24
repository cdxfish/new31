#coding:utf-8
from django import forms
from office.forms import bsSrchFrm

# Create your forms here.

class CnsgnForm(forms.ModelForm):
    from deliver.models import Deliver
    from signtime.models import SignTime

    dlvr = forms.ChoiceField(label=u'配送方式', choices=Deliver.objects.getTupleByAll())
    time = forms.ChoiceField(label=u'收货时间', choices=SignTime.objects.getTupleByAll())

    class Meta:
        from models import Logcs
        from area.models import Area

        model = Logcs
        fields = ('consignee', 'area', 'address', 'tel', 'date', 'note')
        widgets = {
            'address': forms.TextInput(attrs={'size': 70}),
            'tel': forms.TextInput(attrs={'size': 60}),
            'note': forms.Textarea(attrs={'cols': 100, 'rows': 4}),  
            'area': forms.Select(choices=Area.objects.getTupleByAll()),  
            'date': forms.DateInput(attrs={'class': 'date'}, format='%Y-%m-%d'),  
        }


def cnsgnForm(request):
    from views import Cnsgn

    return CnsgnForm(initial={i:v for i, v in Cnsgn(request).c.items()})



class LogcSrchFrm(bsSrchFrm):
    from models import Logcs
    chcs = ((-1, '全部'),) + Logcs.chcs
    c = forms.ChoiceField(label=u'物流状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))



def AdvFrm(o):
    from models import Logcs

    try:
        d = o.logcs.dman.id
    except Exception, e:
        d = 0

    initial = {'advance': o.logcs.advance, 'dman': d}

    class _AdvFrm(bsSrchFrm):
    	try:
    		dman = Role.objects.getDmanToTuple()
    	except Exception, e:
    		dman = ()

    	chcs = tuple([(0, u'物流师傅')] + list(dman))

        advance = forms.ChoiceField(label=u'提前量', choices=Logcs.chcs, widget=forms.Select(attrs={'class': 'ad', 'id': 'a%s' %  o.sn }))
        dman = forms.ChoiceField(label=u'物流师傅', choices=chcs, widget=forms.Select(attrs={'class': 'dman', 'id': 'd%s' %  o.sn }))

    return _AdvFrm(initial=initial)


