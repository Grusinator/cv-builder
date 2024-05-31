from typing import List

import param
import panel as pn
from panel.widgets import TextAreaInput, Button, CrossSelector

from cv_compiler.cv_builder import CVCompiler
from cv_compiler.models import JobPosition


class FetchJobsStep(param.Parameterized):
    info_text = param.String(default='', doc="Personal Information")
    job_description = param.String(default='', doc="Job Description")
    projects = param.List(default=[], doc="Projects")
    jobs = param.List(default=[], doc="Jobs")
    selected_jobs = param.List(default=[], doc="Selected Jobs")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVCompiler()
        self.fetch_button = Button(name='Fetch Jobs', button_type='primary', on_click=self.fetch_info)
        self.cross_selector = CrossSelector(name='Jobs', value=[], options=[])
        self.save_button = Button(name='Select Jobs', button_type='primary', on_click=self.select_jobs)

    @param.depends('jobs', watch=True)
    def update_job_options(self):
        self.cross_selector.options = [job.company for job in self.jobs]

    def view(self):
        return pn.Column(
            "### Fetch and Select Jobs",
            self.fetch_button,
            self.cross_selector,
            self.save_button
        )

    def fetch_info(self, event):
        # Simulate fetching jobs or integrate with an API
        self.jobs: List[JobPosition] = self.cv_compiler.fetch_jobs()
        self.update_job_options()

    def select_jobs(self, event):
        self.selected_jobs = [job for job in self.jobs if job.company in self.cross_selector.value]

    @param.output(jobs=param.List)
    def output(self):
        return self.jobs

    def panel(self):
        return pn.Row(self.view)
