import pytest

from buildcv.models import JobPost
from buildcv.services import FilterRelevantContentService


class TestFilterRelevantContentService:
    def test_find_most_relevant_competencies_to_job_add(self, competencies):
        job_post = JobPost(job_post_text="Deep learning engineer with experience in Python, TensorFlow, and PyTorch")
        filter_service = FilterRelevantContentService()
        relevant_competencies = filter_service.sort_competencies_by_similarity(job_post, competencies)

        expected_competencies = ["deep learning", "Python"]

        # Verify that the names of the relevant competencies match the expected order
        relevant_competency_names = [comp.name for comp in relevant_competencies]
        assert relevant_competency_names[:2] == expected_competencies

    def test_find_most_relevant_projects_to_job_add(self, projects):
        job_post = JobPost(job_post_text="Deep learning engineer with experience in Python, TensorFlow, and PyTorch")
        filter_service = FilterRelevantContentService()
        relevant_projects = filter_service.sort_projects_by_similarity(job_post, projects)

        expected_projects = ["Analyze Me"]

        # Verify that the names of the relevant projects match the expected order
        relevant_project_names = [proj.name for proj in relevant_projects]
        assert relevant_project_names[:1] == expected_projects
