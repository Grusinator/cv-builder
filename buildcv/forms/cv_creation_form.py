from typing import List

from django import forms
from loguru import logger

from buildcv.models import CvCreationProcess, CvTemplate
from cv_content.models import ProjectModel, CompetencyModel, EducationModel, JobPositionModel
from cv_content.schemas import Education, JobPosition, Competency, Project

from typing import List

from django import forms

from buildcv.models import CvCreationProcess, CvTemplate
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
        fields = ['job_positions', 'educations', 'projects', 'competencies']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        initial_competency_ids = kwargs.pop('initial_competency_ids', [])
        initial_project_ids = kwargs.pop('initial_project_ids', [])
        
        super().__init__(*args, **kwargs)
        if user:
            self.fields['projects'].queryset = ProjectModel.objects.filter(user=user)
            self.fields['competencies'].queryset = CompetencyModel.objects.filter(user=user)
            self.fields['job_positions'].queryset = JobPositionModel.objects.filter(user=user)
            self.fields['educations'].queryset = EducationModel.objects.filter(user=user)

            if initial_competency_ids:
                values_list = CompetencyModel.objects.filter(user=user,
                                                             competency_id__in=initial_competency_ids).values_list(
                    'competency_id', flat=True)
                logger.debug(f"competencies: {values_list}")
                self.initial['competencies'] = values_list

            if initial_project_ids:
                project_ids__values_list = ProjectModel.objects.filter(
                    user=user, project_id__in=initial_project_ids).values_list('project_id', flat=True)
                logger.debug("project_select: " + str(project_ids__values_list))
                self.initial['projects'] = project_ids__values_list

            self.initial['job_positions'] = JobPositionModel.objects.filter(user=user).values_list('job_position_id',
                                                                                                   flat=True)
            self.initial['educations'] = EducationModel.objects.filter(user=user).values_list('education_id', flat=True)
        

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


class CvTemplateForm(forms.Form):
    template = forms.ModelChoiceField(queryset=CvTemplate.objects.all(), required=True, label="Select CV Template")
