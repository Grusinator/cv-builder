import pytest
from django.utils import timezone
from cv_content.forms import JobPositionForm


@pytest.mark.django_db
def test_job_position_form_valid_data():
    form_data = {
        'title': 'Senior Developer',
        'company': 'Tech Corp',
        'location': 'Remote',
        'description': 'Develop advanced Django applications.',
        'competencies': 'Python, Django, REST API',  # Simulated JSON-like field
        'start_date': timezone.now().date().isoformat(),
        'end_date': (timezone.now() + timezone.timedelta(days=365)).date().isoformat()
    }
    form = JobPositionForm(data=form_data)
    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_job_position_form_invalid_data():
    form_data = {
        'title': '',  # Invalid as it's required
        'company': 'Tech Corp',
        'location': 'Remote',
        'description': 'Develop advanced Django applications.',
        'competencies': 'Python, Django, REST API',  # Simulated JSON-like field
        'start_date': timezone.now().date().isoformat(),
        'end_date': (timezone.now() - timezone.timedelta(days=365)).date().isoformat()  # Invalid, ends before it starts
    }
    form = JobPositionForm(data=form_data)
    assert not form.is_valid()
    assert 'title' in form.errors  # Should have an error about the title being required
