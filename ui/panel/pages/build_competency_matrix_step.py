import pandas as pd
import panel as pn
import param
from loguru import logger
from panel.widgets import Button, Tabulator

from cv_content.schemas import Competency
from cv_content.services import CVContentCreaterService
from utils.model_utils import ModelUtils


class BuildCompetencyMatrixStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")
    summary = param.String(default='', doc="Summary")
    competencies = param.List(default=[], doc="Competencies")
    jobs = param.List(default=[], doc="Jobs")
    projects = param.List(default=[], doc="Projects")
    educations = param.List(default=[], doc="Educations")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVContentCreaterService()
        self.build_button = Button(name='Build Competencies', button_type='primary', on_click=self.build_competencies)
        self.analyze_button = Button(name='Analyze Competencies', button_type='primary',
                                     on_click=self.update_table_selection_to_match_job_desc)
        competencies = self.cv_compiler.repository.get_competencies()
        competencies_pd = ModelUtils.pydantic_list_to_pandas(competencies, Competency)

        self.table_view = Tabulator(value=competencies_pd, show_index=False, selectable='checkbox', formatters={
            # "last_used": DateFormatter("YYYY"),
            # "years_of_experience": NumberFormatter(format="0.0")
        })

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(
            "### Fetch and Select Jobs",
            self.build_button,
            self.analyze_button,
            self.table_view
        )

    def build_competencies(self, event):
        logger.debug("Building competencies...")
        self.competencies = self.cv_compiler.build_competencies(self.jobs, self.projects)
        self.table_view.value = pd.DataFrame([c.model_dump() for c in self.competencies])

    def update_table_selection_to_match_job_desc(self, event):
        filtered_competencies = self.cv_compiler.match_competencies_with_job_description(self.competencies,
                                                                                         self.job_description,
                                                                                         10)
        self.table_view.selection = self.create_selection_indexes_from_filtered_list(filtered_competencies,
                                                                                     self.competencies)

    def create_selection_indexes_from_filtered_list(self, filtered_list, full_list):
        return [i for i, elm in enumerate(full_list) if elm.name in [filt_elm.name for filt_elm in filtered_list]]

    @param.output(selected_competencies=param.List)
    def output(self):
        self.competencies = ModelUtils.convert_pandas_to_pydantic(self.table_view.value, Competency)
        self.cv_compiler.save_competencies(self.competencies)
        return [comp for i, comp in enumerate(self.competencies) if i in self.table_view.selection]
