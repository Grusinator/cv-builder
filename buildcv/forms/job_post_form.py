from django import forms
from django.forms import DateInput

from ..models import JobPost


class JobPostForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = JobPost
        fields = ['job_post_text', 'job_title', 'company_name', 'recruiter_name', 'contact_email', 'is_freelance',
                  'requisition_number', 'deadline', 'state']
