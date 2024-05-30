import panel as pn

from ui.panel.pages.build_competency_matrix_step import BuildCompetencyMatrixStep
from ui.panel.pages.fetch_jobs_step import FetchJobsStep
from .pages import JobDescriptionStep, FetchProjectsStep, ReviewContentStep, BuildPdfStep

pn.extension('tabulator')


class CVBuilderApp:
    def __init__(self):
        self.pipeline = pn.pipeline.Pipeline(stages=[
            ("Job Description", JobDescriptionStep),
            ("Fetch Projects", FetchProjectsStep),
            ("Fetch jobs", FetchJobsStep),
            ("Build Competency Matrix", BuildCompetencyMatrixStep),
            ("review Content", ReviewContentStep),
            ('Build Pdf', BuildPdfStep),
        ])

    def servable(self):
        return self.pipeline


if __name__.startswith('bokeh'):
    app = CVBuilderApp()
    app.servable().servable()

if __name__ == '__main__':
    app = CVBuilderApp()
    app.servable().show()
