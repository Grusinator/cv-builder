import param
import panel as pn
from panel.widgets import TextAreaInput, Button

from cv_compiler.cv_builder import CVCompiler


class BuildSummaryStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")
    summary = param.String(default='', doc="Summary")
    jobs = param.List(default=[], doc="Jobs")
    projects = param.List(default=[], doc="Projects")
    educations = param.List(default=[], doc="Educations")

    cv_compiler = CVCompiler()

    @param.depends('summary', watch=True)
    def view(self):
        return pn.Column(
            pn.Param(self.param.summary, widgets={
                'summary': {'type': TextAreaInput, 'height': 100}
            }),
            Button(name='Generate Summary', button_type='primary', on_click=self.generate_summary)
        )

    def generate_summary(self, event):
        self.summary = self.cv_compiler.generate_summary(self.job_description, self.jobs, self.educations,
                                                         self.projects)

    @param.output(summary=param.String)
    def output(self):
        return self.summary

    def panel(self):
        return self.view()
