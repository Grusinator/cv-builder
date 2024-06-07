from django.forms import DateInput, DateField

from cv_content.forms.general import ModelFormWithUserInfo
from cv_content.models import EducationModel


class EducationForm(ModelFormWithUserInfo):
    start_date = DateField(
        widget=DateInput(attrs={'type': 'date'}),
        help_text="Select a start date"
    )
    end_date = DateField(
        widget=DateInput(attrs={'type': 'date'}),
        help_text="Select an end date"
    )

    class Meta:
        model = EducationModel
        fields = ['degree', 'school', 'start_date', 'end_date', 'description', 'location']
