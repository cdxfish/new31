#coding:utf-8
from django import forms
# Create your forms here.

def bsInfoFrm(request):

    return BsInfoFrm(initial={
                'sex': request.user.bsinfo.sex,
                'mon': request.user.bsinfo.mon,
                'day': request.user.bsinfo.day,
            })


class BsInfoFrm(forms.ModelForm):

    class Meta:
        from models import BsInfo

        model = BsInfo
        fields = ('sex', 'mon', 'day', 'typ',)
        widgets = {
            'sex': forms.Select(choices=BsInfo.sexs, attrs={'class': 'sex' }),
            'mon': forms.Select(choices=BsInfo.mons, attrs={'class': 'mon' }),
            'day': forms.Select(choices=BsInfo.days, attrs={'class': 'day' }),
            'typ': forms.Select(choices=BsInfo.typs, attrs={'class': 'typ' }),
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
        # widgets = {
        #     'username': forms.TextInput(attrs={'size': 60}),
        #     'last_name': forms.TextInput(attrs={'size': 60}),
        #     'first_name': forms.TextInput(attrs={'size': 60}),
        #     'email': forms.TextInput(attrs={'size': 100}, required=False),
        # }