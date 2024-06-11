import os
import subprocess
import uuid
from typing import Any

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import BaseModel

from buildcv.schemas import CvContent

TEMPLATE_TEX = 'latex_workspace/templates/template1.tex'


class LatexContentBuilderService:

    def __init__(self, base_output_dir='latex_workspace', template_file=TEMPLATE_TEX):
        self.tex_file = 'cv.tex'
        self.base_output_dir = base_output_dir
        self.template_file = template_file

    def build_content(self, cv: CvContent):
        build_id = str(uuid.uuid4())
        output_dir = os.path.join(self.base_output_dir, build_id)
        os.makedirs(output_dir, exist_ok=True)

        cv_escaped = self.escape_latex_in_model(cv)
        context = self.create_context(cv_escaped)
        self.render_template(context, output_dir)
        self.compile_latex(output_dir)
        logger.debug(f"LaTeX content files created successfully in {output_dir}")

    def create_context(self, cv: CvContent):
        return cv.dict()

    def render_template(self, context, output_dir):
        env = Environment(
            loader=FileSystemLoader(os.path.dirname(self.template_file)),
            variable_start_string='((',
            variable_end_string='))'
        )
        env.filters['date_format'] = self.date_format
        template = env.get_template(os.path.basename(self.template_file))
        rendered_content = template.render(context)
        output_tex_file = os.path.join(output_dir, self.tex_file)
        with open(output_tex_file, 'w') as file:
            file.write(rendered_content)

    def compile_latex(self, output_dir):
        tex_file = os.path.join(output_dir, self.tex_file)
        subprocess.run(['pdflatex', '-output-directory', output_dir, tex_file])

    def escape_latex(self, text):
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        return ''.join(replacements.get(char, char) for char in text)

    def escape_latex_in_model(self, model: Any):
        if isinstance(model, BaseModel):
            for field, value in model:
                if isinstance(value, str):
                    setattr(model, field, self.escape_latex(value))
                elif isinstance(value, list):
                    setattr(model, field, [self.escape_latex_in_model(item) for item in value])
                elif isinstance(value, BaseModel):
                    setattr(model, field, self.escape_latex_in_model(value))
        elif isinstance(model, list):
            return [self.escape_latex_in_model(item) for item in model]
        return model

    def date_format(self, value, format='%B %Y'):
        return value.strftime(format)
