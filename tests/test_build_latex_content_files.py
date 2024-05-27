from datetime import datetime

from cv_compiler.build_latex_content_files import LatexContentBuilder
from cv_compiler.models import JobPosition, Competency, GenericProject


def test_create_skill_table_content():
    cv_builder = LatexContentBuilder()

    competencies = [
        Competency(WorkingArea='Software Development', Level=3, LastUsed=2022, YearsOfExp=3),
        Competency(WorkingArea='Databases', Level=4, LastUsed=2021, YearsOfExp=4)
    ]
    expected_content = (
        "\\cvsection{Skill matrix}\n"
        "\\begin{tabular}{|c|c|}\n"
        "\\hline\n"
        "Software Development & Experienced & 2022 & 3 \\\\\n"
        "Databases & Highly experienced & 2021 & 4 \\\\\n"
        "\\end{tabular}"
    )
    content = cv_builder.create_competencies_matrix_table_latex(competencies)
    assert content == expected_content


def test_convert_experiences_to_latex():
    cv_builder = LatexContentBuilder()
    experiences = [
        JobPosition(
            title="Data Engineer",
            company="Energinet",
            start_date=datetime(2022, 12, 1),
            end_date=datetime(2023, 10, 1),
            location="Copenhagen, Denmark",
            description="Developed a data project in Denmark.",
            technologies=["Spark", "Databricks"]
        ),
        JobPosition(
            title="Data Engineer",
            company="Ørsted",
            start_date=datetime(2020, 3, 1),
            end_date=datetime(2022, 11, 1),
            location="Copenhagen, Denmark",
            description="Developed a data validation component.",
            technologies=["Python", "Pandas"]
        )
    ]
    expected_content = (
        """\\cvsection{Experience}
        \\cvevent{Data Engineer}{Energinet}{December 2022 -- October 2023}{Copenhagen, Denmark}
        \\begin{itemize}
        \\item Developed a data project in Denmark
        \\end{itemize}
        \\divider
        \\cvevent{Data Engineer}{Ørsted}{March 2020 -- November 2022}{Copenhagen, Denmark}
        \\begin{itemize}
        \\item Developed a data validation component
        \\end{itemize}
        \\divider"""
    )
    content = cv_builder.convert_experiences_to_latex(experiences)
    assert content == expected_content

def test_create_resume_summary_latex():
    cv_builder = LatexContentBuilder()
    summary_text = "This is a summary of my qualifications and experience."
    expected_content = "\\cvsubsection{Summary}\n\nThis is a summary of my qualifications and experience."
    content = cv_builder.create_summary_latex(summary_text)
    assert content == expected_content


def test_create_projects_latex():
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
    expected_content = ('\\cvsection{Projects}\n'
         '\\cvevent{Project A}{}{}{}\n'
         '\\begin{itemize}\n'
         '\\item This is project A\n'
         '\\end{itemize}\n'
         '\\divider\n'
         '\\cvevent{Project B}{}{}{}\n'
         '\\begin{itemize}\n'
         '\\item This is project B\n'
         '\\end{itemize}\n'
         '\\divider\n')
    content = cv_builder.convert_projects_to_latex(projects)
    assert content == expected_content
