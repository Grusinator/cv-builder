import param
import panel as pn
from panel.widgets import TextAreaInput

from cv_compiler.cv_builder import CVCompiler


class Step1(param.Parameterized):
    info_text = param.String(default='', doc="Personal Information")
    job_description = param.String(default='', doc="Job Description")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_builder = CVCompiler()

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(
            "### Step 1: Fill out Information",
            TextAreaInput(name='Personal Information', value=self.info_text, height=100),
            TextAreaInput(name='Job Description', value=self.job_description, height=100)
        )

    @param.output(('info_text', param.String), ('job_description', param.String))
    def output(self):
        return self.info_text, self.job_description
