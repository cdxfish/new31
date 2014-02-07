# coding: UTF-8
from django import forms

# Create your forms here.


class InvSrchFrm(forms.Form):

    s = forms.DateField(label="起始时间",widget=forms.DateInput(attrs={'class': 'dateNoDir', 'size': 7}, format='%Y-%m-%d'))