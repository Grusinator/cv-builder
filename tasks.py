import invoke

from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder


@invoke.task
def build_content(ctx):
    CVContentBuilder().build_all()


@invoke.task
def build_latex(ctx):
    LatexContentBuilder().build_all()


@invoke.task(build_content, build_latex)
def build(ctx):
    ctx.run("pdflatex -interaction=nonstopmode main.tex")


@invoke.task
def pdflatex(ctx):
    ctx.run("pdflatex main.tex")


if __name__ == '__main__':
    pass
