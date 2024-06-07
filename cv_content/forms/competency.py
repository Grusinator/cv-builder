from cv_content.forms.general import ModelFormWithUserInfo
from cv_content.models import CompetencyModel


class CompetencyForm(ModelFormWithUserInfo):
    class Meta:
        model = CompetencyModel
        fields = ['name', 'level', 'category', 'last_used', 'years_of_experience', 'attractiveness']
