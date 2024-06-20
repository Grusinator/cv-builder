from unittest.mock import MagicMock

import pytest

from buildcv.schemas import JobApplication, CvContent
from cv_content.schemas import JobPosition, Competency, GithubProject, Education
from users.schemas import Profile
from utils.llm_connector import LlmConnector


@pytest.fixture
def mock_llm():
    llm = LlmConnector()
    llm.ask_question = MagicMock(return_value="mocked response")
    llm.try_load_as_json_list = MagicMock(return_value=['Python', 'Java'])
    return llm


@pytest.fixture
def github_projects():
    projects = [
        GithubProject(name="Analyze Me", description="data science project", owner="me", last_commit="2022-11-02",
                      languages=["Python", "JavaScript"],
                      commits=10),
        GithubProject(name="Web app", description="Web development", owner="me", last_commit="2022-11-02",
                      languages=["Java", "C++"], commits=5),
        GithubProject(name="Web project", owner="me", last_commit="2022-11-02", languages=["Python", "HTML"],
                      commits=15),
        GithubProject(name="Report Writing", owner="me", last_commit="2022-11-02", languages=["JavaScript", "CSS"],
                      commits=8),
    ]
    return projects


@pytest.fixture
def projects(github_projects):
    return [project.map_to_generic_project() for project in github_projects]


@pytest.fixture
def job_positions():
    return [
        JobPosition(title="Software Engineer",
                    description="Job description for Software Engineer",
                    location="USA",
                    company="Google",
                    start_date="2019-01-01",
                    end_date="2019-12-31",
                    competencies=["Python", "Problem Solving"]),
        JobPosition(title="Data Scientist",
                    description="Job description for Data Scientist",
                    location="USA",
                    company="Facebook",
                    start_date="2020-01-01",
                    end_date="2020-12-31",
                    competencies=["Python", "Machine Learning"]),
    ]


@pytest.fixture
def competencies():
    competencies = ["Javascript", "SCRUM", "Finance", "reqruiting", "Hunting", "Childcare", "deep learning"]
    return [
        Competency(name='Python', level=1, last_used=2020, years_of_experience=2),
        Competency(name='JavaScript', level=1, last_used=2020, years_of_experience=1),
    ] + [Competency(name=comp, level=3, last_used=2020, years_of_experience=3) for comp in competencies]


@pytest.fixture
def job_app():
    return JobApplication(company_name="Google",
                          job_description="Job description for Software Engineer, requires svelte")


@pytest.fixture
def educations():
    return [
        Education(
            school="University of Copenhagen",
            degree="Master of Science in Computer Science",
            start_date="2017-01-01",
            end_date="2019-01-01",
            location="Copenhagen, Denmark",
            description="Master's thesis on Machine Learning",

        ),
        Education(
            school="University of Copenhagen",
            degree="Bachelor of Science in Computer Science",
            start_date="2014-01-01",
            end_date="2017-01-01",
            location="Copenhagen, Denmark",
            description="Bachelor's thesis on Software Engineering",
        )
    ]


@pytest.fixture
def cv_content(competencies, job_positions, projects, educations):
    summary_text = "Summary text"
    profile = Profile(
        user_id=1,
        birthdate="1990-01-01",
        profile_picture="https://media.licdn.com/dms/image/D4D03AQHckvokGfM_xw/profile-displayphoto-shrink_200_200/0/1667507312442?e=1723680000&v=beta&t=gwfVWUu_7PAUgbYe85YbciDTpUIoHN25Ds_897sbOzs",
        profile_description="Profile description",
        full_name="John Dutton",
        email="test@gmail.com",
        address="Copenhagen, Denmark",
        linkedin="https://www.linkedin.com/in/test",
        github="github.com/test",
        phone_number="+45 12345678"
    )

    job_title = "Software Engineer"
    cv = CvContent(
        job_title=job_title,
        profile=profile, job_positions=job_positions, projects=projects, educations=educations,
        competencies=competencies, summary=summary_text)
    return cv
