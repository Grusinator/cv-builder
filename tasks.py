import invoke
import webbrowser
import os

from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder

from loguru import logger


@invoke.task
def build_content(ctx):
    logger.debug("Building CV content")
    CVContentBuilder().build_all()


@invoke.task
def build_latex(ctx):
    logger.debug("Building LaTeX content")
    LatexContentBuilder().build_all_legacy()


@invoke.task(build_content, build_latex)
def build(ctx):
    ctx.run("pdflatex -interaction=nonstopmode main.tex")


@invoke.task
def pdflatex(ctx):
    ctx.run("pdflatex main.tex")


@invoke.task
def docker_run(ctx):
    ctx.run("docker-compose -f devops/docker/compose.yml up")


@invoke.task
def open_pdf(ctx):
    # Open the PDF in the browser
    pdf_path = "file://" + os.path.join(os.getcwd(), "main.pdf")
    webbrowser.open_new_tab(pdf_path)


@invoke.task
def run_ui(ctx):
    ctx.run("python ui/ui.py")


if __name__ == '__main__':
    pass
