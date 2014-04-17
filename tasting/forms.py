# coding: UTF-8
from django import forms
from models import Apply
# Create your forms here.


class ApplyFrm(forms.ModelForm):

    class Meta:
        model = Apply