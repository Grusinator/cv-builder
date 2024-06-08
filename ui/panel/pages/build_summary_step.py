import param
import panel as pn
from panel.widgets import TextAreaInput, Button

from buildcv.services.generate_summary_service import GenerateSummaryService


class BuildSummaryStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")
    summary = param.String(default='', doc="Summary")
    jobs = param.List(default=[], doc="Jobs")
    projects = param.List(default=[], doc="Projects")
    educations = param.List(default=[], doc="Educations")



    @param.depends('summary', watch=True)
    def view(self):
        return pn.Column(
            pn.Param(self.param.summary, widgets={
                'summary': {'type': TextAreaInput, 'height': 100}
            }),
            Button(name='Generate Summary', button_type='primary', on_click=self.generate_summary)
        )

    def generate_summary(self, event):
        service = GenerateSummaryService()
        self.summary = service.generate_summary_from_llm(self.job_description, self.jobs, self.educations,
                                                         self.projects)

    @param.output(summary=param.String)
    def output(self):
        return self.summary

    def panel(self):
        return self.view()
