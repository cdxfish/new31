#coding:utf-8
from django import forms
# Create your forms here.

def setFrm(request):

    return SetFrm()
    # return setFrm(initial= )



class SetFrm(forms.Form):
    from models import UserInfo

    # user = forms.CharField(label=u'用户名', )
    sex = forms.ChoiceField(label=u'性别', choices=UserInfo.sexs, widget=forms.Select(attrs={'class': 'sex' }))
    mon = forms.ChoiceField(label=u'月',  choices=UserInfo.mons, widget=forms.Select(attrs={'class': 'mon' }))
    day = forms.ChoiceField(label=u'日',  choices=UserInfo.days, widget=forms.Select(attrs={'class': 'day' }))


def pwdFrm(request):

    return PwdFrm()
    
class PwdFrm(forms.Form):
    oPwd = forms.CharField(label=u'当前密码', widget=forms.PasswordInput(attrs={'class': 'oPwd' }))
    nPwd = forms.CharField(label=u'新密码', widget=forms.PasswordInput(attrs={'class': 'nPwd' }))
    cPwd = forms.CharField(label=u'确认密码', widget=forms.PasswordInput(attrs={'class': 'cPwd' }))