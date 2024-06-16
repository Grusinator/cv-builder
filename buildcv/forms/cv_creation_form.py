from django import forms
from django.core.serializers import serialize
from buildcv.models import CvCreationProcess
from cv_content.models import ProjectModel, CompetencyModel, EducationModel, JobPositionModel
from cv_content.schemas import Education, JobPosition, Competency, Project


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
            jobs = JobPositionModel.objects.filter(user=user)
            self.fields['job_positions'].queryset = jobs
            self.fields["job_positions"].initial = jobs.values_list('job_position_id', flat=True)
            self.fields['educations'].queryset = EducationModel.objects.filter(user=user)

    def clean_projects(self):
        projects = self.cleaned_data.get('projects')
        return Project.dict_from_orm_list(projects)

    def clean_competencies(self):
        competencies = self.cleaned_data.get('competencies')
        return Competency.dict_from_orm_list(competencies)

    def clean_job_positions(self):
        job_positions = self.cleaned_data.get('job_positions')
        return JobPosition.dict_from_orm_list(job_positions)

    def clean_educations(self):
        educations = self.cleaned_data.get('educations')
        return Education.dict_from_orm_list(educations)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.projects = self.cleaned_data['projects']
        instance.competencies = self.cleaned_data['competencies']
        instance.job_positions = self.cleaned_data['job_positions']
        instance.educations = self.cleaned_data['educations']
        if commit:
            instance.save()
        return instance
