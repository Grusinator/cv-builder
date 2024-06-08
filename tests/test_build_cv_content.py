from cv_content.services.extract_cv_content_from_pdf_service import ExtractCvContentFromPdfService
from cv_content.schemas import Competency, GithubProject


class TestBuildCvContent:

    def test_filter_most_relevant_projects(self):
        cv_content_builder = ExtractCvContentFromPdfService()
        projects = [
            GithubProject(name="Project 1", owner="me", last_commit="2022-11-02", languages=["Python", "JavaScript"],
                          commits=10),
            GithubProject(name="Project 2", owner="me", last_commit="2022-11-02", languages=["Java", "C++"], commits=5),
            GithubProject(name="Project 3", owner="me", last_commit="2022-11-02", languages=["Python", "HTML"],
                          commits=15),
            GithubProject(name="Project 4", owner="me", last_commit="2022-11-02", languages=["JavaScript", "CSS"],
                          commits=8),
        ]
        competencies = [
            Competency(name='Python', level=0, last_used=2020, years_of_experience=2),
            Competency(name='JavaScript', level=0, last_used=2020, years_of_experience=1),
        ]
        expected_projects = [
            GithubProject(name="Project 3", owner="me", last_commit="2022-11-02", languages=["Python", "HTML"],
                          commits=15),
            GithubProject(name="Project 1", owner="me", last_commit="2022-11-02", languages=["Python", "JavaScript"],
                          commits=10),
        ]
        filtered_projects = cv_content_builder.filter_most_relevant_projects(projects, competencies)
        assert filtered_projects == expected_projects
