# coding: UTF-8
from django import forms
from models import Apply, ApplyArea
# Create your forms here.


class ApplyFrm(forms.ModelForm):

    class Meta:
        model = Apply

        widgets = {
            'area': forms.Select(choices=((i.area.get_name_display(), i.area.get_name_display()) \
                for i in ApplyArea.objects.filter(onl=True) )  ),
        }