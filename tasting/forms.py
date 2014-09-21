# coding: UTF-8
from django import forms
from models import Apply, ApplyArea
from office.forms import bsSrchFrm
# Create your forms here.


class ApplyFrm(forms.ModelForm):

    class Meta:
        model = Apply

        widgets = {
            'area': forms.Select(choices=((i.area.get_name_display(), i.area.get_name_display()) \
                for i in ApplyArea.objects.filter(onl=True) )  ),
        }


class AppSrchFrm(forms.Form):
    from models import Apply, Discuss
    chcs = ((-1, '全部'),) + Discuss.chcs
    tchcs = ((-1, '全部'),) + Apply.chcs
    schcs = ((-1, '全部'),) + Apply._chcs


    c = forms.ChoiceField(label=u'洽谈状态', choices=chcs, widget=forms.Select(attrs={'class': 'c' }))
    t = forms.ChoiceField(label=u'时间安排', choices=tchcs, widget=forms.Select(attrs={'class': 't' }))
    s = forms.ChoiceField(label=u'公司规模', choices=schcs, widget=forms.Select(attrs={'class': 's' }))
    k = forms.CharField(label=u'关键字', required=False)
