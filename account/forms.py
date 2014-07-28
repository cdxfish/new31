# coding: UTF-8
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re
# Create your forms here.

def bsInfoFrm(request):

    return BsInfoFrm(initial={
                'sex': request.user.bsinfo.sex,
                'mon': request.user.bsinfo.mon,
                'day': request.user.bsinfo.day,
            })


class _BsInfoFrm(forms.ModelForm):

    class Meta:
        from models import BsInfo

        model = BsInfo
        fields = ('mon', 'day',)
        widgets = {
            'mon': forms.Select(choices=BsInfo.mons, attrs={'class': 'mon' }),
            'day': forms.Select(choices=BsInfo.days, attrs={'class': 'day' }),
        }

    def clean_mon(self):
        mon = self.cleaned_data['mon']

        if not mon:
            raise forms.ValidationError(u'请填写正确的生月!')

        return mon

    def clean_day(self):
        day = self.cleaned_data['day']

        if not day:
            raise forms.ValidationError(u'请填写正确的生日!')

        return day

class BsInfoFrm(forms.ModelForm):

    class Meta:
        from models import BsInfo

        model = BsInfo
        fields = ('sex', 'typ', 'mon', 'day',)
        widgets = {
            'sex': forms.Select(choices=BsInfo.sexs, attrs={'class': 'sex' }),
            'typ': forms.Select(choices=BsInfo.typs, attrs={'class': 'typ' }),
            'mon': forms.Select(choices=BsInfo.mons, attrs={'class': 'mon' }),
            'day': forms.Select(choices=BsInfo.days, attrs={'class': 'day' }),
        }

class PtsFrm(forms.ModelForm):

    class Meta:
        from models import Pts

        model = Pts
        fields = ('pt', )

class NerUserFrm(forms.ModelForm):

    class Meta:
        from django.contrib.auth.models import User

        model = User
        fields = ('username', 'last_name', 'first_name', 'email',)

    def clean_username(self):
        from models import BsInfo
        username = self.cleaned_data['username']

        if not re.match(BsInfo.ure, username):
            raise forms.ValidationError(u'请填写正确的手机号码!')

        return username

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if len(last_name) > 2:
            raise forms.ValidationError(u'请填写正确的姓氏!')

        return last_name


class EditUserFrm(NerUserFrm):
    username = forms.CharField(label=u'用户名')

    class Meta:
        from django.contrib.auth.models import User

        model = User
        fields = ('last_name', 'first_name', 'email',)


class QuicklyNewUserFrm(NerUserFrm, UserCreationForm):
    def __init__(self, *args, **kwarg):
        super(QuicklyNewUserFrm, self).__init__(*args, **kwarg)

class UserSrechFrm(forms.Form):
    k = forms.CharField(label=u'关键字', required=False)