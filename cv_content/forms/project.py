from cv_content.forms.general import ModelFormWithUserInfo, CommaSeparatedInput
from cv_content.models import ProjectModel


class ProjectForm(ModelFormWithUserInfo):
    competencies = CommaSeparatedInput(
        help_text="Enter competencies separated by commas"
    )

    class Meta:
        model = ProjectModel
        fields = ['name', 'description', 'effort_in_years', 'competencies']