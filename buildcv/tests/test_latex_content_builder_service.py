import textwrap
from datetime import datetime

from buildcv.schemas import CvContent
from buildcv.services.latex_content_builder_service import LatexContentBuilderService
from cv_content.schemas import JobPosition, Competency, Project


class TestLatexContentBuilder:

    def test_render_template(self, cv_content: CvContent, file_regression):
        latex_builder = LatexContentBuilderService(template_file="latex_workspace/templates/template1.tex")
        latex_builder.render_template(cv_content, output_dir="latex_workspace")
        file_regression.check(open("latex_workspace/cv.tex").read(), extension=".tex")


    def test_build_content(self, cv_content: CvContent, file_regression):
        latex_builder = LatexContentBuilderService(template_file="latex_workspace/templates/template1.tex")
        latex_builder.build_content(cv_content)