import os
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import BaseModel

from buildcv.schemas import CvContent

TEMPLATE_TEX = Path('latex_workspace/templates/template1.tex')


class BuildLatexCVService:
    base_output_dir: Path = Path('latex_workspace/cv_generation')

    def build_cv_from_content(self, cv: CvContent, template_file: Path = TEMPLATE_TEX):
        output_tex_file_path = self.base_output_dir / str(uuid.uuid4()) / f'cv.tex'
        os.makedirs(output_tex_file_path.parent, exist_ok=True)
        context = self.prepare_context(cv)
        self.render_template(context, output_tex_file_path, template_file)
        pdf_path = self.compile_latex_to_pdf(output_tex_file_path)
        logger.debug(f"LaTeX content file created successfully in {output_tex_file_path}")
        pdf_file = self.load_pdf(pdf_path)
        # os.remove(output_tex_file_path.parent)
        return pdf_file

    def prepare_context(self, cv: CvContent) -> Dict[str, Any]:
        cv_escaped = self.escape_latex_in_model(cv)
        context = cv_escaped.dict()
        return context

    def render_template(self, context, output_tex_file, template_file: Path):
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Rendering template: {template_file}, to {output_tex_file}")
        env = Environment(
            loader=FileSystemLoader(template_file.parent),
            variable_start_string='((',
            variable_end_string='))'
        )
        env.filters['date_format'] = self.date_format
        template = env.get_template(template_file.name)
        rendered_content = template.render(context)
        with open(output_tex_file, 'w') as file:
            file.write(rendered_content)

    def compile_latex_to_pdf(self, tex_file_path: Path):
        command = f"pdflatex -interaction=nonstopmode -output-directory {tex_file_path.parent} {tex_file_path.name}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logger.debug(result.stdout)
        logger.debug("return code: " + str(result.returncode))
        logger.debug(result.stderr)
        if result.returncode != 1 and ("error" in result.stderr.lower()):
            logger.error(result.stderr)
            raise Exception(f"Error building CV: \n {result.stderr}")
        else:
            logger.info("CV successfully built")
            return tex_file_path.with_suffix('.pdf')

    def load_pdf(self, path: Path) -> bytes:
        with open(path, "rb") as f:
            return f.read()

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
