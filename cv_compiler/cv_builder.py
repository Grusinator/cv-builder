from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder


class CVCompiler:

    def __init__(self):
        self.content_builder = CVContentBuilder()
        self.latex_builder = LatexContentBuilder()

    def build_cv(self):
        self.content_builder.build_all()
        self.latex_builder.build_all()
        self.build_latex_cv()

    def build_latex_cv(self):
        # run pdflatex main.tex
        pass


if __name__ == '__main__':
    cv_compiler = CVCompiler()
    cv_compiler.build_cv()
