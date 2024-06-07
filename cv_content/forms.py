from django import forms
from django.forms.widgets import DateInput

from cv_content.models import JobPositionModel


class CommaSeparatedInput(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]

    def prepare_value(self, value):
        if isinstance(value, list):
            return ', '.join(value)
        return value


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Upload a PDF', help_text='Select a PDF file',
                           widget=forms.FileInput(attrs={'accept': 'application/pdf'}))


class JobPositionForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',
                               None)  # Extract user from kwargs and ensure it does not interfere with other form data
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user_id = self.user.id  # Assign the user ID to the instance
        if commit:
            instance.save()
            self.save_m2m()  # Ensure many-to-many fields are saved
        return instance
