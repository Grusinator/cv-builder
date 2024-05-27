from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.models import Competency, JobPosition


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
            Competency(WorkingArea='Python', Level=0, LastUsed=2020, YearsOfExp=2),
            Competency(WorkingArea='Problem Solving', Level=0, LastUsed=2019, YearsOfExp=1),
            Competency(WorkingArea='Machine Learning', Level=0, LastUsed=2020, YearsOfExp=1)
        ]
        generated_competencies = cv_content_builder.generate_competencies_from_job_positions(job_positions)
        assert generated_competencies == expected_competencies
