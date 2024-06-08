import panel as pn
import param
from panel.widgets import Button, FileInput, JSONEditor


from cv_content.schemas import JobPosition, Education
from cv_content.services import CVContentCreaterService


class FetchJobsAndEducationStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")
    projects = param.List(default=[], doc="Projects")
    jobs = param.List(default=[], doc="Jobs")
    educations = param.List(default=[], doc="Educations")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVContentCreaterService()
        self.pdf_file_upload = FileInput(accept=".pdf", name="Upload PDF")
        self.load_from_pdf_button = Button(name='Load from PDF', button_type='primary', on_click=self.load_from_pdf)
        self.jobs_editor = JSONEditor(value=[job.dict() for job in self.jobs], mode="tree")
        self.educations_editor = JSONEditor(value=[edu.dict() for edu in self.educations], mode="tree")

    def panel(self):
        return self.view()

    def view(self):
        return pn.Column(
            "### Fetch and edit job positions and educations, "
            "download the PDF from linkedin or other sources and upload it here.",
            self.pdf_file_upload,
            self.load_from_pdf_button,
            pn.Row(
                pn.Column(
                    "### Jobs",
                    self.jobs_editor),
                pn.Column(
                    "### Educations",
                    self.educations_editor
                )
            )
        )

    def load_from_pdf(self, event):
        pdf = self.pdf_file_upload.value
        self.educations = self.cv_compiler.load_educations_from_pdf(pdf)
        self.jobs = self.cv_compiler.load_job_positions_from_pdf(pdf)
        self.jobs_editor.value = [job.dict() for job in self.jobs]
        self.educations_editor.value = [edu.dict() for edu in self.educations]

    @param.output(jobs=param.List, educations=param.List)
    def output(self):
        self.jobs = [JobPosition(**j) for j in self.jobs_editor.value]
        self.educations = [Education(**e) for e in self.educations_editor.value]
        return self.jobs, self.educations
