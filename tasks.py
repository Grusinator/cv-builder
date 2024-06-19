import os
import webbrowser
from pathlib import Path

import invoke

docker_path = Path("devops/docker")


@invoke.task
def pdflatex(ctx):
    ctx.run("pdflatex main.tex")


@invoke.task
def docker_run(ctx, env=""):
    base_compose = docker_path / "docker-compose.yml"
    env_compose = docker_path / f"docker-compose.{env}.yml"
    ctx.run(f"docker-compose -f {base_compose} -f {env_compose} up --build")


@invoke.task
def open_pdf(ctx):
    # Open the PDF in the browser
    pdf_path = "file://" + os.path.join(os.getcwd(), "main.pdf")
    webbrowser.open_new_tab(pdf_path)


@invoke.task
def run_panel(ctx):
    ctx.run("panel serve --show cv_app.py --autoreload --port 5006")


@invoke.task
def terraform(ctx):
    ctx.run("terraform -chdir=devops/terraform init")
    ctx.run("terraform -chdir=devops/terraform plan")


if __name__ == '__main__':
    pass
