import textwrap
from typing import List

from cv_compiler.file_handler import FileHandler
from cv_compiler.models import GenericProject, JobPosition, Competency

CONTENT_EXPERIENCE_TEX = 'cv_latex_content/experience.tex'
CONTENT_SUMMARY_TEX = "cv_latex_content/summary.tex"
CONTENT_SKILL_MATRIX_TEX = "cv_latex_content/skill_matrix.tex"


class LatexContentBuilder:

    def __init__(self):
        self.file_handler = FileHandler()

    def build_all(self):
        self.create_competencies_matrix_latex()
        self.create_job_experiences_latex()
        self.create_projects_latex()
        self.create_resume_summary_latex()

    def create_resume_summary_latex(self):
        summary_text = self.file_handler.read_summary_txt_file()
        latex_content = self.create_summary_latex(summary_text)
        self.write_to_file(CONTENT_SUMMARY_TEX, latex_content)

    def create_summary_latex(self, summary_text):
        return "\\cvsubsection{Summary}\n\n" + summary_text

    def create_projects_latex(self):
        github_projects = self.file_handler.read_generated_projects_from_csv()
        generic_projects = [proj.map_to_generic_project() for proj in github_projects]
        latex_content = self.convert_projects_to_latex(generic_projects)
        self.write_to_file('cv_latex_content/projects.tex', latex_content)

    def convert_projects_to_latex(self, projects: List[GenericProject]) -> str:
        latex_content = "\\cvsection{Projects}\n"

        for project in projects:
            latex_content += "\\cvevent{" + project.name + "}{}{}{}\n\\begin{itemize}\n"
            latex_content += "\\item " + project.description + "\n"
            latex_content += "\\end{itemize}\n\\divider\n"

        return latex_content

    def create_job_experiences_latex(self):
        job_experiences = self.file_handler.get_background_job_positions()
        job_positions_latex = self.convert_experiences_to_latex(job_experiences)
        self.write_to_file(CONTENT_EXPERIENCE_TEX, job_positions_latex)

    def write_to_file(self, output_file, content):
        with open(output_file, 'w+') as file:
            file.write(content)

    def create_competencies_matrix_latex(self):
        competencies = self.file_handler.read_generated_competencies_from_csv()
        latex_content = self.create_competencies_matrix_table_latex(competencies)
        self.write_to_file(CONTENT_SKILL_MATRIX_TEX, latex_content)

    def create_competencies_matrix_table_latex(self, table_data: List[Competency]) -> str:
        rows = [self.create_latex_competency_matrix_row(competency) for competency in table_data]
        joined_rows = ("\n" + " " * 8).join(rows)  # indent each row by 8 spaces, to make dedent work properly

        table_structure = f"""
        \\cvsection{{Skill matrix}}
        \\begin{{tabular}}{{|c|c|}}
        \\hline
        {joined_rows}
        \\end{{tabular}}
        """
        return textwrap.dedent(table_structure).lstrip()

    def create_latex_competency_matrix_row(self, competency: Competency):
        row = [competency.name, competency.level_description, competency.last_used, competency.years_of_experience]
        content = " & ".join(self.convert_special_chars(str(value)) for value in row) + " \\\\"
        return content

    def write_skill_table_as_latex(self, output_file, table_data):
        content = self.create_competencies_matrix_table_latex(table_data)
        self.write_to_file(output_file, content)

    def convert_experiences_to_latex(self, job_positions: List[JobPosition]) -> str:
        latex_content = "\\cvsection{Experience}"
        for job in job_positions:
            latex_content += self.create_job_position_section(job)
        return latex_content

    def create_job_position_section(self, job: JobPosition):
        start_date = job.start_date.strftime('%B %Y')
        end_date = job.end_date.strftime('%B %Y')
        competency_tags = " ".join([f"\\cvtag{{{tech}}}" for tech in job.technologies])
        text = f"""
            \\cvevent{{{job.title}}}{{{job.company}}}{{{start_date} -- {end_date}}}{{{job.location}}}
            \\begin{{itemize}}
            {job.description}
            \\end{{itemize}}
            {competency_tags}
            \\divider
        """
        return textwrap.dedent(text)

    def convert_special_chars(self, string):
        return (
            string
            .replace("_", "\\_")
            .replace("#", "\\#")
        )


if __name__ == '__main__':
    latex_builder = LatexContentBuilder()
    latex_builder.build_all()
