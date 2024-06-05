import os

import panel as pn

from ui.panel.pages.build_competency_matrix_step import BuildCompetencyMatrixStep
from ui.panel.pages.build_summary_step import BuildSummaryStep
from ui.panel.pages.fetch_jobs_step import FetchJobsAndEducationStep
from .pages import JobDescriptionStep, FetchProjectsStep, ReviewContentStep, BuildPdfStep

pn.extension('tabulator', 'ace', 'jsoneditor')


class CVBuilderApp:
    def __init__(self):
        self.pipeline = pn.pipeline.Pipeline(stages=[
            ("Job Description", JobDescriptionStep),
            ("Fetch Projects", FetchProjectsStep),
            ("Fetch jobs", FetchJobsAndEducationStep),
            ("Build Summary", BuildSummaryStep),
            ("Build Competency Matrix", BuildCompetencyMatrixStep),
            ("review Content", ReviewContentStep),
            ('Build Pdf', BuildPdfStep),
        ], debug=os.getenv("PANEL_DEBUG") == "True", inherit_params=True)

    def view(self):
        return pn.Row(self.pipeline)


if __name__.startswith('bokeh'):
    app = CVBuilderApp()
    app.view().servable()

if __name__ == '__main__':
    app = CVBuilderApp()
    app.view().show()
