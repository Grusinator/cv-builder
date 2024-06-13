import invoke
import webbrowser
import os

from buildcv.services.latex_content_builder_service import BuildLatexCVService
from cv_content.services.extract_cv_content_from_pdf_service import ExtractCvContentFromPdfService

from loguru import logger


@invoke.task
def build_content(ctx):
    logger.debug("Building CV content")
    ExtractCvContentFromPdfService().build_all()


@invoke.task
def build_latex(ctx, template=None):
    logger.debug("Building LaTeX content")
    raise NotImplementedError("This task is not implemented")
    BuildLatexCVService(template_file=None).build_cv_from_content()


@invoke.task(build_content, build_latex)
def build(ctx, file="main.tex"):
    ctx.run(f"pdflatex -interaction=nonstopmode {file}")


@invoke.task
def pdflatex(ctx):
    ctx.run("pdflatex main.tex")


@invoke.task
def docker_run(ctx):
    ctx.run("docker-compose -f devops/docker/compose.yml up --build")


@invoke.task
def open_pdf(ctx):
    # Open the PDF in the browser
    pdf_path = "file://" + os.path.join(os.getcwd(), "main.pdf")
    webbrowser.open_new_tab(pdf_path)


@invoke.task
def run_ui(ctx):
    ctx.run("panel serve --show cv_app.py --autoreload --port 5006")

@invoke.task
def terraform(ctx):
    ctx.run("terraform -chdir=devops/terraform init")
    ctx.run("terraform -chdir=devops/terraform plan")

if __name__ == '__main__':
    pass
