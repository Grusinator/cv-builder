from django.forms import DateField, DateInput

from cv_content.forms.cv_content_util_forms import ModelFormWithUserInfo, CommaSeparatedInput
from cv_content.models import ProjectModel


class ProjectForm(ModelFormWithUserInfo):
    competencies = CommaSeparatedInput(
        help_text="Enter competencies separated by commas"
    )
    last_updated = DateField(
        widget=DateInput(attrs={'type': 'date'}),
        help_text="Select a start date"
    )

    class Meta:
        model = ProjectModel
        fields = ['name', 'description', 'effort_in_years', 'competencies', "last_updated"]
