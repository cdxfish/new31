# coding: UTF-8
from django import forms

# Create your forms here.

class LogcsFrm(forms.ModelForm):
    from deliver.models import Deliver
    from signtime.models import SignTime

    dlvr = forms.ChoiceField(label=u'配送方式', choices=Deliver.objects.getTpl())
    time = forms.ChoiceField(label=u'收货时间', choices=SignTime.objects.getTpl())

    class Meta:
        from models import Logcs
        from area.models import Area

        model = Logcs
        fields = ('consignee', 'area', 'address', 'tel', 'date', 'note')
        widgets = {
            'address': forms.TextInput(attrs={'size': 70}),
            'tel': forms.TextInput(attrs={'size': 60}),
            'note': forms.Textarea(attrs={'cols': 100, 'rows': 4}),
            'area': forms.Select(choices=Area.objects.getTpl()),
            'date': forms.DateInput(attrs={'class': 'date'}, format='%Y-%m-%d'),
        }


def logcsFrm(request):
    from views import LogcSess

    return LogcsFrm(initial=LogcSess(request).sess)


from office.forms import bsSrchFrm
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

    from purview.models import Role
    try:
        ds = Role.objects.getDmanToTuple()
    except Exception, e:
        ds = ()

    advance = forms.ChoiceField(label=u'提前量', choices=Logcs.advs, widget=forms.Select(attrs={'class': 'ad', 'id': 'a%s' %  o.sn }))
    dman = forms.ChoiceField(label=u'物流师傅', choices=tuple([(0, u'物流师傅')] + list(ds)), widget=forms.Select(attrs={'class': 'dman', 'id': 'd%s' %  o.sn }))

    return type('_AdvFrm', (bsSrchFrm,), {'advance': advance, 'dman': dman})(initial=initial)