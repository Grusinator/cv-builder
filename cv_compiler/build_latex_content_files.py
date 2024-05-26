import re
from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

from cv_compiler.models import JobPosition


class BuildLatexContentFiles:

    def convert_competencies_matrix_csv_to_latex(self, csv_file, output_file):
        table_data = self.read_skill_csv_file(csv_file)
        self.write_skill_table_as_latex(output_file, table_data)

    def create_skill_table_content(self, table_data: pd.DataFrame) -> str:
        content = "\\cvsection{Skill matrix}\n"
        content += "\\begin{tabular}{|c|c|}\n"
        content += "\\hline\n"
        table_data = table_data[['Working Area', "Level", "Last Used", "Years of exp"]]
        for row in table_data.itertuples(index=False):
            content += " & ".join(str(value) for value in row) + " \\\\\n"
        content += "\\end{tabular}"
        return content

    def write_to_file(self, output_file, content):
        with open(output_file, 'w+') as file:
            file.write(content)

    def write_skill_table_as_latex(self, output_file, table_data):
        content = self.create_skill_table_content(table_data)
        self.write_to_file(output_file, content)

    def convert_experiences_to_latex(self, experiences: List[JobPosition]) -> str:
        latex_content = "\\cvsection{Experience}\n"

        for experience in experiences:
            latex_content += "\\cvevent{" + experience.title + "}{" + experience.company + "}{" + \
                             experience.start_date.strftime('%B %Y') + " -- " + \
                             (experience.end_date.strftime('%B %Y') if experience.end_date != datetime.now() else "Present") + \
                             "}{" + experience.location + "}\n\\begin{itemize}\n"

            for item in experience.description.split('.'):
                if item:  # Avoid empty bullet points
                    latex_content += "\\item " + item.strip() + "\n"

            latex_content += "\\end{itemize}\n\\divider\n"

        return latex_content

    def read_skill_csv_file(self, csv_file) -> pd.DataFrame:
        table_data = pd.read_csv(csv_file)
        return table_data

    def scrape_job_application_text(self, job_application_text_file, table_data):
        with open(job_application_text_file, 'r') as file:
            job_text = file.read()

        skills = table_data['Working Area'].tolist()
        matched_skills = []

        for skill in skills:
            pattern = re.compile(r'\b{}\b'.format(skill), re.IGNORECASE)
            if pattern.search(job_text):
                matched_skills.append(skill)

        return matched_skills

    def write_matching_skills_to_file(self, matched_skills):
        with open('matching_skills.txt', 'w') as file:
            for skill in matched_skills:
                file.write(skill + '\n')
