import re

import pandas as pd


def convert_csv_to_latex(csv_file, output_file):
    table_data = read_skill_csv_file(csv_file)
    write_skill_table_as_latex(output_file, table_data)


def write_skill_table_as_latex(output_file, table_data):
    with open(output_file, 'w+') as file:
        file.write("\\cvsection{Skill matrix}\n")
        file.write("\\begin{tabular}{|c|c|}\n")
        file.write("\\hline\n")
        table_data = table_data[['Working Area', "Level","Last Used","Years of exp"]]
        for row in table_data.itertuples(index=False):
            file.write(" & ".join(str(value) for value in row) + " \\\\\n")
        file.write("\\end{tabular}")


def read_skill_csv_file(csv_file) -> pd.DataFrame:
    table_data = pd.read_csv(csv_file)
    return table_data


def scrape_job_application_text(job_application_text_file, table_data):
    with open(job_application_text_file, 'r') as file:
        job_text = file.read()

    skills = table_data['Working Area'].tolist()
    matched_skills = []

    for skill in skills:
        pattern = re.compile(r'\b{}\b'.format(skill), re.IGNORECASE)
        if pattern.search(job_text):
            matched_skills.append(skill)

    return matched_skills


def write_matching_skills_to_file(matched_skills):
    for skill in matched_skills:
        with open('matching_skills.txt', 'w') as file:
            for skill in matched_skills:
                file.write(skill + '\n')


