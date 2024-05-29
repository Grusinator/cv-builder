from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder
import subprocess

from loguru import logger

from cv_compiler.file_handler import FileHandler


class CVCompiler:
    output_pdf_path = "main.pdf"

    def __init__(self, file_handler=FileHandler()):
        self.file_handler = file_handler
        self.content_builder = CVContentBuilder(self.file_handler)
        self.latex_builder = LatexContentBuilder(self.file_handler)

    def build_cv(self):
        self.content_builder.build_all()
        self.latex_builder.build_all()
        self.build_latex_cv()
        return "main.pdf"

    def build_latex_cv(self):
        command = "pdflatex -interaction=nonstopmode main.tex"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
        else:
            logger.info("CV successfully built")


if __name__ == '__main__':
    cv_compiler = CVCompiler()
    cv_compiler.build_cv()
