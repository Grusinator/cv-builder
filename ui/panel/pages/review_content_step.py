import panel as pn
import param
from panel.widgets import CrossSelector


class ReviewContentStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")
    summary = param.String(default='', doc="Summary")
    competencies = param.List(default=[], doc="Competencies")
    jobs = param.List(default=[], doc="Jobs")
    projects = param.List(default=[], doc="Projects")
    educations = param.List(default=[], doc="Educations")

    selected_jobs = param.List(default=[], doc="Selected Jobs")
    selected_projects = param.List(default=[], doc="Selected Projects")
    selected_educations = param.List(default=[], doc="Selected Educations")

    selected_competencies = param.List(default=[], doc="Selected Competencies")

    def __init__(self, **params):
        super().__init__(**params)
        project_options = [proj.name for proj in self.projects]
        self.projects_cross_selector = CrossSelector(name='Projects', value=[], options=project_options)

        job_options = [job.unique_id for job in self.jobs]
        self.jobs_cross_selector = CrossSelector(name='Jobs', value=[], options=job_options)

        educations_options = [edu.degree for edu in self.educations]
        self.educations_cross_selector = CrossSelector(name='Educations', value=[], options=educations_options)

    def panel(self):
        return self.view()

    def view(self):
        return pn.Column(
            "### Select Projects",
            self.projects_cross_selector,
            "### Select Jobs",
            self.jobs_cross_selector,
            "### Select Educations",
            self.educations_cross_selector
        )

    @param.output(selected_projects=param.List, selected_jobs=param.List, selected_educations=param.List)
    def output(self):
        self.selected_educations = [e for e in self.educations if e.degree in self.educations_cross_selector.options]
        self.selected_projects = [p for p in self.projects if p.name in self.projects_cross_selector.options]
        self.selected_jobs = [j for j in self.jobs if j.unique_id in self.jobs_cross_selector.options]
        return self.selected_projects, self.selected_jobs, self.selected_educations
