import param
import panel as pn
from panel.widgets import TextAreaInput

from cv_compiler.cv_builder import CVCompiler


class JobDescriptionStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_builder = CVCompiler()

    def panel(self):
        return pn.Row(self.view)

    @param.depends("job_description")
    def view(self):
        return pn.Column(
            pn.Param(self.param.job_description, widgets={
                'job_description': {'type': TextAreaInput, 'height': 100}
            })
        )

    @param.output(job_description=param.String)
    def output(self):
        return self.job_description
