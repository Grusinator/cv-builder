import pytest
from mock.mock import MagicMock

from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.models import Competency, GithubProject, JobPosition


class TestBuildCvContent:

    def test_generate_competencies_from_job_positions(self):
        cv_content_builder = CVContentBuilder()
        job_positions = [
            JobPosition(title="Software Engineer",
                        description="Job description for Software Engineer",
                        location="USA",
                        company="Google",
                        start_date="2019-01-01",
                        end_date="2019-12-31",
                        technologies=["Python", "Problem Solving"]),
            JobPosition(title="Data Scientist",
                        description="Job description for Data Scientist",
                        location="USA",
                        company="Facebook",
                        start_date="2020-01-01",
                        end_date="2020-12-31",
                        technologies=["Python", "Machine Learning"]),
        ]
        expected_competencies = [
            Competency(name='Python', level=0, last_used=2020, years_of_experience=2),
            Competency(name='Problem Solving', level=0, last_used=2019, years_of_experience=1),
            Competency(name='Machine Learning', level=0, last_used=2020, years_of_experience=1)
        ]
        generated_competencies = cv_content_builder.generate_competencies_from_job_positions(job_positions)
        assert generated_competencies == expected_competencies

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

    @pytest.mark.parametrize("competency_names, expected_matched_competencies", [
        (['Python'], ['Python']),
        (['python'], ['Python']),
        (["Delta-lake"], ["Delta Lake"]),
        (['Java', 'C++', 'HTML', 'CSS'], []),
        (['Python', 'JavaScript'], ['Python', 'JavaScript']),
    ])
    def test_filter_union_of_competencies(self, competency_names, expected_matched_competencies):
        cv_content_builder = CVContentBuilder()

        competencies = [
            Competency(name='Python', level=0, last_used=2020, years_of_experience=2),
            Competency(name='JavaScript', level=0, last_used=2020, years_of_experience=1),
        ]
        union_of_competencies = cv_content_builder.filter_union_of_competencies(competencies, competency_names)
        assert {comp.name for comp in union_of_competencies} == set(expected_matched_competencies)

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
