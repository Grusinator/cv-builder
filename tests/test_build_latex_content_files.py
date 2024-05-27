from datetime import datetime

from cv_compiler.build_latex_content_files import LatexContentBuilder
from cv_compiler.models import JobPosition, Competency


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
