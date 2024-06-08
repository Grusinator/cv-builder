from django import forms
from django.forms.widgets import DateInput

from cv_content.forms.cv_content_util_forms import CommaSeparatedInput, ModelFormWithUserInfo
from cv_content.models import JobPositionModel


class JobPositionForm(ModelFormWithUserInfo):
    competencies = CommaSeparatedInput(
        help_text="Enter competencies separated by commas"
    )
    start_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        help_text="Select a start date"
    )
    end_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        help_text="Select an end date"
    )

    class Meta:
        model = JobPositionModel
        fields = ['title', 'company', 'location', 'start_date', 'end_date', 'description', 'competencies']
