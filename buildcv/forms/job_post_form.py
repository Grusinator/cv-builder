from django import forms
from ..models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['job_post_text', 'job_title', 'company_name', 'recruiter_name', 'contact_email', 'is_freelance',
                  'requisition_number']
