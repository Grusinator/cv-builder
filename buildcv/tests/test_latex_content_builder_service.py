from buildcv.schemas import CvContent
from buildcv.services.build_latex_cv_service import BuildLatexCVService


class TestLatexContentBuilder:

    def test_render_template(self, cv_content: CvContent, file_regression):
        latex_builder = BuildLatexCVService(template_file="latex_workspace/templates/template1.tex")
        output_tex_file = "latex_workspace/test.tex"
        latex_builder.render_template(cv_content, output_tex_file)
        file_regression.check(open(output_tex_file).read(), extension=".tex")


    def test_build_content(self, cv_content: CvContent, file_regression):
        latex_builder = BuildLatexCVService(template_file="latex_workspace/templates/template1.tex")
        latex_builder.build_cv_from_content(cv_content)