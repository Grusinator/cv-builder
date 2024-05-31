import pytest
from mock.mock import MagicMock

from cv_compiler.llm_connector import ChatGPTInterface
from cv_compiler.models import GithubProject, JobPosition, Competency, JobApplication


@pytest.fixture
def mock_llm():
    llm = ChatGPTInterface()
    llm.ask_question = MagicMock(return_value="mocked response")
    llm.try_load_as_json_list = MagicMock(return_value=['Python', 'Java'])
    return llm


@pytest.fixture
def github_projects():
    projects = [
        GithubProject(name="Project 1", owner="me", last_commit="2022-11-02", languages=["Python", "JavaScript"],
                      commits=10),
        GithubProject(name="Project 2", owner="me", last_commit="2022-11-02", languages=["Java", "C++"], commits=5),
        GithubProject(name="Project 3", owner="me", last_commit="2022-11-02", languages=["Python", "HTML"],
                      commits=15),
        GithubProject(name="Project 4", owner="me", last_commit="2022-11-02", languages=["JavaScript", "CSS"],
                      commits=8),
    ]
    return projects


@pytest.fixture
def job_positions():
    return [
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


@pytest.fixture
def competencies():
    return [
        Competency(name='Python', level=1, last_used=2020, years_of_experience=2),
        Competency(name='JavaScript', level=1, last_used=2020, years_of_experience=1),
    ]


@pytest.fixture
def job_app():
    return JobApplication(company_name="Google",
                          job_description="Job description for Software Engineer, requires svelte")
