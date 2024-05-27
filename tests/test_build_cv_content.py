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
            Competency(WorkingArea='Python', Level=0, LastUsed=2020, YearsOfExp=2),
            Competency(WorkingArea='Problem Solving', Level=0, LastUsed=2019, YearsOfExp=1),
            Competency(WorkingArea='Machine Learning', Level=0, LastUsed=2020, YearsOfExp=1)
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
            Competency(WorkingArea='Python', Level=0, LastUsed=2020, YearsOfExp=2),
            Competency(WorkingArea='JavaScript', Level=0, LastUsed=2020, YearsOfExp=1),
        ]
        expected_projects = [
            GithubProject(name="Project 3", owner="me", last_commit="2022-11-02", languages=["Python", "HTML"],
                          commits=15),
            GithubProject(name="Project 1", owner="me", last_commit="2022-11-02", languages=["Python", "JavaScript"],
                          commits=10),
        ]
        filtered_projects = cv_content_builder.filter_most_relevant_projects(projects, competencies)
        assert filtered_projects == expected_projects
