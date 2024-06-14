import os
from buildcv.schemas import CvContent
from buildcv.services.build_latex_cv_service import BuildLatexCVService


class TestLatexContentBuilder:

    def test_render_template(self, cv_content: CvContent, file_regression):
        latex_builder = BuildLatexCVService()
        output_tex_file = "latex_workspace/test.tex"
        latex_builder.render_template(cv_content, output_tex_file)
        file_regression.check(open(output_tex_file).read(), extension=".tex")

    def test_build_content(self, cv_content: CvContent):
        latex_builder = BuildLatexCVService()
        # latex_builder.compile_latex_to_pdf = lambda x: "latex_workspace/cv.pdf"
        latex_builder.build_cv_from_content(cv_content)
        assert os.path.exists("latex_workspace/cv.pdf")