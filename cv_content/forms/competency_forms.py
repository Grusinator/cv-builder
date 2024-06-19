from datetime import datetime

from django.forms import modelformset_factory, ChoiceField, RadioSelect, IntegerField, \
    HiddenInput, FloatField

from cv_content.forms.cv_content_util_forms import ModelFormWithUserInfo
from cv_content.models import CompetencyModel


class BaseCompetencyForm(ModelFormWithUserInfo):
    LAST_USED_YEARS = [(str(year), str(year)) for year in range(datetime.now().year, datetime.now().year - 8, -1)]

    LEVEL_CHOICES = [(str(i), str(i)) for i in range(1, 6)]
    last_used = ChoiceField(choices=LAST_USED_YEARS)
    level = ChoiceField(choices=LEVEL_CHOICES, widget=RadioSelect)
    years_of_experience = FloatField(min_value=0, max_value=30)

    class Meta:
        model = CompetencyModel
        fields = ['name']


class ListCompetencyForm(ModelFormWithUserInfo):
    LAST_USED_YEARS = [(str(year), str(year)) for year in range(datetime.now().year, datetime.now().year - 8, -1)]

    LEVEL_CHOICES = [(str(i), str(i)) for i in range(1, 6)]
    last_used = ChoiceField(choices=LAST_USED_YEARS)
    level = ChoiceField(choices=LEVEL_CHOICES, widget=RadioSelect)
    years_of_experience = FloatField(min_value=0, max_value=30)
    competency_id = IntegerField(widget=HiddenInput())

    class Meta:
        model = CompetencyModel
        fields = ["competency_id", 'level', 'last_used', 'years_of_experience']


CompetencyFormSet = modelformset_factory(CompetencyModel, form=ListCompetencyForm, extra=0)


class CompetencyForm(BaseCompetencyForm):

    class Meta:
        model = CompetencyModel
        fields = ['name', 'level', 'last_used', 'years_of_experience']
