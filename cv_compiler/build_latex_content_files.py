import textwrap
from typing import List

from cv_compiler.file_handler import FileHandler
from cv_compiler.models import GenericProject, JobPosition, Competency

CONTENT_PROJECTS_TEX = 'cv_latex_content/projects.tex'
CONTENT_EXPERIENCE_TEX = 'cv_latex_content/experience.tex'
CONTENT_SUMMARY_TEX = "cv_latex_content/summary.tex"
CONTENT_SKILL_MATRIX_TEX = "cv_latex_content/skill_matrix.tex"

from loguru import logger


class LatexContentBuilder:

    def __init__(self, file_handler=FileHandler()):
        self.file_handler = file_handler

    def build_all(self):
        self.create_competencies_matrix_latex()
        self.create_job_experiences_latex()
        self.create_projects_latex()
        self.create_resume_summary_latex()
        logger.debug("Latex content files created successfully")

    def write_to_file(self, output_file, content):
        with open(output_file, 'w+', encoding='utf-8') as file:
            file.write(content)

    def create_resume_summary_latex(self):
        summary_text = self.file_handler.read_summary_txt_file()
        latex_content = self.create_summary_latex(summary_text)
        self.write_to_file(CONTENT_SUMMARY_TEX, latex_content)

    def create_summary_latex(self, summary_text):
        sumary = f"""
        \\cvsubsection{{Summary}}\n
        {self.convert_special_chars(self.wrap_lines_dot(summary_text))}
        """
        return textwrap.dedent(sumary).lstrip()

    def wrap_lines_dot(self, text):
        # for readability, add a newline after each dot, so lines are shorter
        return text.replace(".", ".\n" + " " * 8)

    def create_projects_latex(self):
        github_projects = self.file_handler.read_generated_projects_from_json()
        generic_projects = [proj.map_to_generic_project() for proj in github_projects]
        latex_content = self.convert_projects_to_latex(generic_projects)
        self.write_to_file(CONTENT_PROJECTS_TEX, latex_content)

    def convert_projects_to_latex(self, projects: List[GenericProject]) -> str:
        latex_content = "\\cvsection{Projects}\n"
        projects_latex = [self.create_project_latex(project) for project in projects]
        return latex_content + "\\divider\n\n".join(projects_latex)

    def create_project_latex(self, project: GenericProject) -> str:
        competency_tags = self.create_list_of_competency_tags(project.competencies)
        project = textwrap.dedent(
            f"""
            \\cvevent{{{project.name}}}{{}}{{}}{{}}
            {self.convert_special_chars(self.wrap_lines_dot(project.description))}
            {competency_tags}
            """
        ).lstrip()
        return project

    def create_job_experiences_latex(self):
        job_experiences = self.file_handler.get_background_job_positions()
        job_positions_latex = self.convert_experiences_to_latex(job_experiences)
        self.write_to_file(CONTENT_EXPERIENCE_TEX, job_positions_latex)

    def create_competencies_matrix_latex(self):
        competencies = self.file_handler.read_generated_competencies_from_csv()
        latex_content = self.create_competencies_matrix_table_latex(competencies)
        self.write_to_file(CONTENT_SKILL_MATRIX_TEX, latex_content)

    def create_competencies_matrix_table_latex(self, table_data: List[Competency]) -> str:
        rows = [self.create_latex_competency_matrix_row(competency) for competency in table_data]
        joined_rows = ("\n" + " " * 8).join(rows)  # indent each row by 8 spaces, to make dedent work properly

        table_structure = f"""
        \\cvsection{{Skill matrix}}
        \\begin{{tabular}}{{|c|c|c|c|}}
        \\hline
        name & level & last used & years of exp. \\\\
        \\hline
        {joined_rows}
        \\end{{tabular}}
        """
        return textwrap.dedent(table_structure).lstrip()

    def create_latex_competency_matrix_row(self, competency: Competency):
        row = [
            f"\\textbf{{{self.convert_special_chars(competency.name)}}}",
            f"\\cvskill{{}}{{{competency.level}}}",
            int(competency.last_used),
            int(competency.years_of_experience)
        ]
        content = " & ".join(str(cell) for cell in row) + " \\\\"
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
        technologies = job.technologies
        competency_tags = self.create_list_of_competency_tags(technologies)
        text = f"""
        \\cvevent{{{job.title}}}{{{job.company}}}{{{start_date} -- {end_date}}}{{{job.location}}}
        {self.convert_special_chars(self.wrap_lines_dot(job.description))}
        {competency_tags}
        \\divider
        """
        return textwrap.dedent(text)

    def create_list_of_competency_tags(self, competency_names: List[str]):
        return " ".join([f"\\cvtag{{{tech}}}" for tech in competency_names])

    def convert_special_chars(self, string):
        return (
            string
            .replace("_", "\\_")
            .replace("#", "\\#")
        )


if __name__ == '__main__':
    latex_builder = LatexContentBuilder()
    latex_builder.build_all()
