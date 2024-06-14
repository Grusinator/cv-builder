import os
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict

from django.conf import settings
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import BaseModel
import requests
from django.core.files.storage import default_storage
from pathlib import Path
import shutil
from buildcv.schemas import CvContent
from django.utils._os import safe_join

TEMPLATE_TEX = Path('latex_workspace/templates/template1.tex')


class BuildLatexCVService:
    profile_picture_filename = "profile_picture.jpg"
    base_output_dir: Path = Path('latex_workspace/cv_generation')
    base_tex_file_name = 'cv.tex'

    def build_cv_from_content(self, cv_context: CvContent, template_file: Path = TEMPLATE_TEX, media_content=None):
        workspace_folder_path = self.create_workspace_folder(prefix=f"{cv_context.job_title.replace(' ', '_')}")
        self.save_media(media_content, workspace_folder_path)
        context = self.prepare_context(cv_context)
        tex_file_path = self.render_template(context, workspace_folder_path, template_file)
        pdf_path = self.compile_latex_to_pdf(tex_file_path)
        pdf_file = self.load_pdf(pdf_path)
        # os.remove(output_tex_file_path.parent)
        return pdf_file

    def create_workspace_folder(self, prefix="cv") -> Path:
        workspace_folder_path = self.base_output_dir / f"{prefix}_{str(uuid.uuid4())[:8]}"
        workspace_folder_path.mkdir(parents=False, exist_ok=True)
        return workspace_folder_path

    def save_media(self, media_content: Dict[str, bytes], path: Path):
        if media_content:
            for fn, file_bytes in media_content.items():
                with open(path / fn, "wb") as file:
                    file.write(file_bytes)

    def prepare_context(self, cv_context: CvContent) -> Dict[str, Any]:
        cv_escaped = self.escape_latex_in_model(cv_context)
        context = cv_escaped.model_dump()
        return context

    def render_template(self, context, workspace_folder, template_file: Path):
        output_tex_file = workspace_folder / self.base_tex_file_name
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
        return output_tex_file

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
            logger.debug(f"LaTeX content file created successfully in {tex_file_path}")
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

    def date_format(self, value, format='%b. %Y'):
        return value.strftime(format)
