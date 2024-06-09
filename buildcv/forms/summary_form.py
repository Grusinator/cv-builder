# forms.py
from django import forms
from buildcv.models import CvCreationProcess


class SummaryForm(forms.ModelForm):
    class Meta:
        model = CvCreationProcess
        fields = ['summary']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
