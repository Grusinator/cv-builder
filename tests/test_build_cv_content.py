import pytest
from mock.mock import MagicMock

from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.models import Competency, GithubProject, JobPosition


class TestBuildCvContent:

    def test_filter_most_relevant_projects(self):
        cv_content_builder = CVContentBuilder()
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



    def test_build_all_mocked(self):
        cv_content_builder = CVContentBuilder()
        cv_content_builder.chatgpt_interface.ask_question = MagicMock(return_value='["Python", "JavaScript"]')
        projects = [
            GithubProject(name="Project 1", owner="me", last_commit="2022-11-02", languages=["Python", "JavaScript"],
                          commits=10),
            GithubProject(name="Project 2", owner="me", last_commit="2022-11-02", languages=["Java", "C++"], commits=5),
            GithubProject(name="Project 3", owner="me", last_commit="2022-11-02", languages=["Python", "HTML"],
                          commits=15),
            GithubProject(name="Project 4", owner="me", last_commit="2022-11-02", languages=["JavaScript", "CSS"],
                          commits=8),
        ]
        cv_content_builder.github_fetcher.get_github_projects = MagicMock(return_value=projects)
        cv_content_builder.build_all()
