import textwrap
from datetime import datetime

from cv_compiler.build_latex_content_files import LatexContentBuilder
from cv_compiler.models import JobPosition, Competency, GenericProject


class TestLatexContentBuilder:
    def test_create_skill_table_content(self):
        cv_builder = LatexContentBuilder()

        competencies = [
            Competency(name='Software Development', level=3, last_used=2022, years_of_experience=3),
            Competency(name='Databases', level=4, last_used=2021, years_of_experience=4)
        ]
        expected_content = textwrap.dedent(
            """
            \\cvsection{Skill matrix}
            \\begin{tabular}{|c|c|}
            \\hline
            Software Development & Experienced & 2022 & 3 \\\\
            Databases & Highly experienced & 2021 & 4 \\\\
            \\end{tabular}
            """
        ).lstrip()
        content = cv_builder.create_competencies_matrix_table_latex(competencies)
        assert content == expected_content

    def test_convert_experiences_to_latex(self):
        cv_builder = LatexContentBuilder()
        experiences = [
            JobPosition(
                title="Data Engineer",
                company="Energinet",
                start_date=datetime(2022, 12, 1),
                end_date=datetime(2023, 10, 1),
                location="Copenhagen",
                description="Developed a data project in Denmark.",
                technologies=["Spark", "Databricks"]
            ),
            JobPosition(
                title="Data Engineer",
                company="Ørsted",
                start_date=datetime(2020, 3, 1),
                end_date=datetime(2022, 11, 1),
                location="Copenhagen",
                description="Developed a data validation component.",
                technologies=["Python", "Pandas"]
            )
        ]
        expected_content = textwrap.dedent(
            """            
            \\cvsection{Experience}
            \\cvevent{Data Engineer}{Energinet}{December 2022 -- October 2023}{Copenhagen}
            \\begin{itemize}
            Developed a data project in Denmark.
            \\end{itemize}
            \\cvtag{Spark} \\cvtag{Databricks}
            \\divider

            \\cvevent{Data Engineer}{Ørsted}{March 2020 -- November 2022}{Copenhagen}
            \\begin{itemize}
            Developed a data validation component.
            \\end{itemize}
            \\cvtag{Python} \\cvtag{Pandas}
            \\divider
            """
        ).lstrip()
        content = cv_builder.convert_experiences_to_latex(experiences)
        assert content == expected_content

    def test_create_resume_summary_latex(self):
        cv_builder = LatexContentBuilder()
        summary_text = "This is a summary of my qualifications and experience."
        expected_content = "\\cvsubsection{Summary}\n\nThis is a summary of my qualifications and experience."
        content = cv_builder.create_summary_latex(summary_text)
        assert content == expected_content

    def test_create_projects_latex(self):
        cv_builder = LatexContentBuilder()

        projects = [
            GenericProject(
                name="Project A",
                description="This is project A",
                effort_in_years=1,
                competencies=["Python", "Django"]
            ),
            GenericProject(
                name="Project B",
                description="This is project B",
                effort_in_years=0.5,
                competencies=["JavaScript", "React"]
            )
        ]
        expected_content = textwrap.dedent(
            """
            \\cvsection{Projects}
            \\cvevent{Project A}{}{}{}
            \\begin{itemize}
            \\item This is project A
            \\end{itemize}
            \\divider
            \\cvevent{Project B}{}{}{}
            \\begin{itemize}
            \\item This is project B
            \\end{itemize}
            \\divider
            """
        ).lstrip()

        content = cv_builder.convert_projects_to_latex(projects)
        assert content == expected_content

    def test_build_all(self):
        cv_builder = LatexContentBuilder()
        cv_builder.build_all()
