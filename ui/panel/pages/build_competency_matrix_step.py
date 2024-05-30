import pandas as pd
import panel as pn
import param
from bokeh.models import DateFormatter, NumberFormatter
from loguru import logger
from panel.widgets import Button, Tabulator

from cv_compiler.cv_builder import CVCompiler


class BuildCompetencyMatrixStep(param.Parameterized):
    job_description = param.String(default='', doc="Job Description")
    projects = param.List(default=[], doc="Jobs")
    jobs = param.List(default=[], doc="Selected Jobs")
    competencies = param.List(default=[], doc="Competencies")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVCompiler()
        self.build_button = Button(name='Build Competencies', button_type='primary', on_click=self.build_competencies)

        self.table_view = Tabulator(show_index=False, selectable='checkbox', formatters={
            # "last_used": DateFormatter("YYYY"),
            # "years_of_experience": NumberFormatter(format="0.0")
        })

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(
            "### Fetch and Select Jobs",
            self.build_button,
            self.table_view
        )

    def build_competencies(self, event):
        # TODO should get them from prev steps.
        # self.projects = self.cv_compiler.file_handler.read_generated_projects_from_json()
        # self.jobs = self.cv_compiler.file_handler.get_background_job_positions()
        # self.job_description = self.cv_compiler.file_handler.get_job_description()
        # logger.debug("Building competencies...")
        # logger.debug(f"job description: {self.job_description}")
        # logger.debug(f"jobs: {self.jobs}")
        # logger.debug(f"projects: {self.projects}")
        # self.competencies = self.cv_compiler.build_competencies(self.job_description, self.jobs,
        #                                                         self.projects)
        self.competencies = self.cv_compiler.file_handler.get_background_competency_matrix()
        self.table_view.value = pd.DataFrame([c.dict() for c in self.competencies])
