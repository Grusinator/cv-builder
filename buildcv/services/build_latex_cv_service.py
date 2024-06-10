import subprocess

from loguru import logger


from buildcv.schemas import CvContent
from buildcv.services.latex_content_builder_service import LatexContentBuilderService


class BuildLatexCVService:
    output_pdf_path = "main.pdf"

    def __init__(self):
        self.latex_content_builder = LatexContentBuilderService()

    def build_cv_from_content(self, content: CvContent):
        self.latex_content_builder.build_content(content)
        pdf_file = self.build_latex_cv()
        return pdf_file

    def build_latex_cv(self):
        command = "pdflatex -interaction=nonstopmode main.tex"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logger.debug(result.stdout)
        logger.debug("return code: " + str(result.returncode))
        logger.debug(result.stderr)
        if result.returncode != 0:
            logger.error(result.stderr)
            raise Exception(f"Error building CV: \n {result.stderr}")
        else:
            logger.info("CV successfully built")
            return self.load_pdf()

    def load_pdf(self):
        with open(self.output_pdf_path, "rb") as f:
            return f.read()
