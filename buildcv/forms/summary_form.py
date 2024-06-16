# forms.py
from django import forms
from buildcv.models import CvCreationProcess


class SummaryForm(forms.ModelForm):
    class Meta:
        model = CvCreationProcess
        fields = ['summary_guidance','summary']
        widgets = {
            'summary_guidance': forms.Textarea(attrs={'rows': 8, 'cols': 40}),
            'summary': forms.Textarea(attrs={'rows': 8, 'cols': 40}),
        }
