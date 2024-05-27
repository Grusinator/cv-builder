from datetime import datetime
from typing import List

from cv_compiler.file_handler import FileHandler
from cv_compiler.models import GenericProject, JobPosition, Competency

CONTENT_SUMMARY_TEX = "cv_latex_content/summary.tex"
SKILL_MATRIX_TEX = "cv_latex_content/skill_matrix.tex"


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
        job_experiences = self.file_handler.get_job_positions()
        self.convert_experiences_to_latex(job_experiences)

    def write_to_file(self, output_file, content):
        with open(output_file, 'w+') as file:
            file.write(content)

    def create_competencies_matrix_latex(self):
        competencies = self.file_handler.read_generated_competencies_from_csv()
        latex_content = self.create_competencies_matrix_table_latex(competencies)
        self.write_to_file(SKILL_MATRIX_TEX, latex_content)

    def create_competencies_matrix_table_latex(self, table_data: List[Competency]) -> str:
        content = "\\cvsection{Skill matrix}\n"
        content += "\\begin{tabular}{|c|c|}\n"
        content += "\\hline\n"
        for competency in table_data:
            row = [competency.WorkingArea, competency.level_description, competency.LastUsed, competency.YearsOfExp]
            content += " & ".join(str(value) for value in row) + " \\\\\n"
        content += "\\end{tabular}"
        return content

    def write_skill_table_as_latex(self, output_file, table_data):
        content = self.create_competencies_matrix_table_latex(table_data)
        self.write_to_file(output_file, content)

    def convert_experiences_to_latex(self, experiences: List[JobPosition]) -> str:
        latex_content = "\\cvsection{Experience}\n"

        for experience in experiences:
            latex_content += "\\cvevent{" + experience.title + "}{" + experience.company + "}{" + \
                             experience.start_date.strftime('%B %Y') + " -- " + \
                             (experience.end_date.strftime(
                                 '%B %Y') if experience.end_date != datetime.now() else "Present") + \
                             "}{" + experience.location + "}\n\\begin{itemize}\n"

            for item in experience.description.split('.'):
                if item:  # Avoid empty bullet points
                    latex_content += "\\item " + item.strip() + "\n"

            latex_content += "\\end{itemize}\n\\divider\n"

        return latex_content


