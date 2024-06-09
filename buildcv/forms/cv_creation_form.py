from django import forms
from django.core.serializers import serialize
from buildcv.models import CvCreationProcess
from cv_content.models import ProjectModel, CompetencyModel, EducationModel, JobPositionModel


class CvContentForm(forms.ModelForm):
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
        fields = ['projects', 'competencies', 'job_positions', 'educations']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['projects'].queryset = ProjectModel.objects.filter(user=user)
            self.fields['competencies'].queryset = CompetencyModel.objects.filter(user=user)
            self.fields['job_positions'].queryset = JobPositionModel.objects.filter(user=user)
            self.fields['educations'].queryset = EducationModel.objects.filter(user=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.projects = serialize('json', self.cleaned_data['projects'])
        instance.competencies = serialize('json', self.cleaned_data['competencies'])
        instance.job_positions = serialize('json', self.cleaned_data['job_positions'])
        instance.educations = serialize('json', self.cleaned_data['educations'])
        if commit:
            instance.save()
        return instance
