import pytest

from cv_compiler.competency_matrix_calculator import CompetencyMatrixCalculator
from cv_compiler.file_handler import FileHandler
from cv_compiler.llm_connector import ChatGPTInterface
from cv_compiler.models import JobPosition, Competency


class TestCompetencyMatrixCalculator:

    def test_build(self):
        fh = FileHandler()
        jobs = fh.get_background_job_positions()
        llm = ChatGPTInterface()
        background_competencies = fh.get_background_competency_matrix()
        projects = fh.read_generated_projects_from_json()
        job_app = fh.read_job_application()
        calc = CompetencyMatrixCalculator(llm)
        competencies = calc.build(jobs, projects, job_app, background_competencies)
        assert competencies

    def test_generate_competencies_from_job_positions(self, mock_llm):
        competency_calculator = CompetencyMatrixCalculator(mock_llm)
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
            Competency(name='Python', level=1, last_used=2020, years_of_experience=2),
            Competency(name='Problem Solving', level=1, last_used=2019, years_of_experience=1),
            Competency(name='Machine Learning', level=1, last_used=2020, years_of_experience=1)
        ]
        generated_competencies = competency_calculator.generate_competencies_from_job_positions(job_positions)
        assert generated_competencies == expected_competencies
