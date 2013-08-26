#coding:utf-8
from django import forms
# Create your forms here.

def setFrm(request):

    return SetFrm(initial={
                'sex': request.user.bsinfo.sex,
                'mon': request.user.bsinfo.mon,
                'day': request.user.bsinfo.day,
            })



class SetFrm(forms.Form):
    from models import BsInfo

    sex = forms.ChoiceField(label=u'性别', choices=BsInfo.sexs, widget=forms.Select(attrs={'class': 'sex' }))
    mon = forms.ChoiceField(label=u'月',  choices=BsInfo.mons, widget=forms.Select(attrs={'class': 'mon' }))
    day = forms.ChoiceField(label=u'日',  choices=BsInfo.days, widget=forms.Select(attrs={'class': 'day' }))