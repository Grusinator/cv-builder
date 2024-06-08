from django import forms

from buildcv.models import CvCreationProcess
from cv_content.models import ProjectModel, CompetencyModel, EducationModel, JobPositionModel


class CvCreationForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        queryset=ProjectModel.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    competencies = forms.ModelMultipleChoiceField(
        queryset=CompetencyModel.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    job_positions = forms.ModelMultipleChoiceField(
        queryset=JobPositionModel.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    educations = forms.ModelMultipleChoiceField(
        queryset=EducationModel.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CvCreationProcess
        fields = ['summary', 'projects', 'competencies', 'job_positions', 'educations']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['projects'].queryset = ProjectModel.objects.filter(user=user)
            self.fields['competencies'].queryset = CompetencyModel.objects.filter(user=user)
            self.fields['job_positions'].queryset = JobPositionModel.objects.filter(user=user)
            self.fields['educations'].queryset = EducationModel.objects.filter(user=user)


