import invoke

from cv_compiler.build_latex import convert_csv_to_latex, read_skill_csv_file, scrape_job_application_text, \
    write_matching_skills_to_file

default_csv_file = 'data/competencies_old.csv'
default_output_file = 'cv_content/skill_matrix.tex'
job_application_text_file = 'job_application_text.txt'


@invoke.task
def csv_to_latex(ctx, csv_file=default_csv_file, output_file=default_output_file):
    convert_csv_to_latex(csv_file, output_file)


@invoke.task
def scrape_job_text(ctx, csv_file=default_csv_file, job_text_file=job_application_text_file):
    table_data = read_skill_csv_file(csv_file)
    matched_skills = scrape_job_application_text(job_text_file, table_data)
    write_matching_skills_to_file(matched_skills)


@invoke.task
def build(ctx):
    ctx.run("python tasks.py csv_to_latex")
    ctx.run("python tasks.py scrape_job_text")
    ctx.run("pdflatex main.tex")


if __name__ == '__main__':
    convert_csv_to_latex(default_csv_file, default_output_file)
