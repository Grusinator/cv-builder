import invoke
import webbrowser
import os

from buildcv.services.latex_content_builder_service import LatexContentBuilderService
from cv_content.services.extract_cv_content_from_pdf_service import ExtractCvContentFromPdfService

from loguru import logger


@invoke.task
def build_content(ctx):
    logger.debug("Building CV content")
    ExtractCvContentFromPdfService().build_all()


@invoke.task
def build_latex(ctx):
    logger.debug("Building LaTeX content")
    raise NotImplementedError("This task is not implemented")
    LatexContentBuilderService().build_content()


@invoke.task(build_content, build_latex)
def build(ctx):
    ctx.run("pdflatex -interaction=nonstopmode main.tex")


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


if __name__ == '__main__':
    pass
