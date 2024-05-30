import param
import panel as pn
from unittest.mock import MagicMock
from panel.widgets import Button, TextAreaInput
from panel.pane import Markdown

from cv_compiler.cv_builder import CVCompiler


class Step4(param.Parameterized):
    job_application = param.String(default='', doc="Job Application Text")
    build_status = param.String(default='', doc="Build Status")
    pdf_viewer = pn.pane.PDF(width=800, height=800)
    download_button = pn.widgets.FileDownload(filename='output.pdf', button_type='primary', width=200)
    compiler = CVCompiler()

    def __init__(self, **params):
        super().__init__(**params)
        self.build_button = Button(name='Build CV', button_type='primary')
        self.build_button.on_click(self.build_cv)

    def panel(self):
        return pn.Row(self.view)

    @param.depends('build_status', "pdf_viewer")
    def view(self):
        return pn.Column(
            "### Step 4: Build and Review",
            TextAreaInput(name='Job Application', value=self.job_application, height=200),
            self.build_button,
            Markdown(self.build_status),
            self.pdf_viewer,
            self.download_button
        )

    def build_cv(self, event):
        self.build_status = "Building CV..."
        self.compiler.parse_job_application(self.job_application)
        output_pdf = self.compiler.load_pdf()  # TODO revert back to running the process for real
        self.pdf_viewer.object = output_pdf
        self.download_button.file = output_pdf
        self.build_status = "CV built successfully!"
