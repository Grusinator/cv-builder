from django import forms
from django.forms import ModelForm


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


class ModelFormWithUserInfo(ModelForm):
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
