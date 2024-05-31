import pandas as pd
import panel as pn
import param
from loguru import logger
from panel.widgets import Button, Tabulator

from cv_compiler.cv_builder import CVCompiler


class BuildCompetencyMatrixStep(param.Parameterized):
    job_description = param.String(default='', doc="Job Description")
    projects = param.List(default=[], doc="Projects")
    jobs = param.List(default=[], doc="Jobs")
    competencies = param.List(default=[], doc="Competencies")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVCompiler()
        self.build_button = Button(name='Build Competencies', button_type='primary', on_click=self.build_competencies)
        self.analyze_button = Button(name='Analyze Competencies', button_type='primary',
                                     on_click=self.analyze_competencies)

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
            self.analyze_button,
            self.table_view
        )

    def analyze_competencies(self, event):
        filtered_competencies = self.cv_compiler.match_competencies_with_job_description(self.competencies,
                                                                                         self.job_description,
                                                                                         10)
        self.table_view.selection = self.create_selection_indexes_from_filtered_list(filtered_competencies,
                                                                                     self.competencies)

    def create_selection_indexes_from_filtered_list(self, filtered_list, full_list):
        return [i for i, elm in enumerate(full_list) if elm.name in [filt_elm.name for filt_elm in filtered_list]]

    def build_competencies(self, event):
        logger.debug("Building competencies...")
        self.competencies = self.cv_compiler.build_competencies(self.job_description, self.jobs,
                                                                self.projects)
        self.table_view.value = pd.DataFrame([c.dict() for c in self.competencies])

    @param.output(selected_competencies=param.List)
    def output(self):
        return [comp for i, comp in enumerate(self.competencies) if i in self.table_view.selection]
