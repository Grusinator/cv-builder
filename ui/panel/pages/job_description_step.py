import param
import panel as pn
from panel.widgets import TextAreaInput

from cv_compiler.cv_builder import CVCompiler


class JobDescriptionStep(param.Parameterized):
    info_text = param.String(default='', doc="Personal Information")
    job_description = param.String(default='test123', doc="Job Description")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_builder = CVCompiler()

    def panel(self):
        return pn.Row(self.view)

    @param.depends("info_text", "job_description")
    def view(self):
        return pn.Column(
            "### Step 1: Fill out Information",
            pn.Param(self.param.info_text, widgets={
                'info_text': {'type': TextAreaInput, 'height': 100}
            }),
            pn.Param(self.param.job_description, widgets={
                'job_description': {'type': TextAreaInput, 'height': 100}
            })
        )

    @param.output(info_text=param.String, job_description=param.String)
    def output(self):
        return self.info_text, self.job_description
