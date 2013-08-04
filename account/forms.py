#coding:utf-8
from django import forms
# Create your forms here.

def setFrm(request):

    return SetFrm(initial={
                'sex': request.user.userinfo.sex,
                'mon': request.user.userinfo.mon,
                'day': request.user.userinfo.day,
            })



class SetFrm(forms.Form):
    from models import UserInfo

    sex = forms.ChoiceField(label=u'性别', choices=UserInfo.sexs, widget=forms.Select(attrs={'class': 'sex' }))
    mon = forms.ChoiceField(label=u'月',  choices=UserInfo.mons, widget=forms.Select(attrs={'class': 'mon' }))
    day = forms.ChoiceField(label=u'日',  choices=UserInfo.days, widget=forms.Select(attrs={'class': 'day' }))