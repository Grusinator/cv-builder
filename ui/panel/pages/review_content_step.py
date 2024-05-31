import param
import panel as pn
from panel.widgets import TextAreaInput, JSONEditor


class ReviewContentStep(param.Parameterized):
    projects = param.List(default=[], doc="Projects")
    jobs = param.List(default=[], doc="Jobs")
    competencies = param.List(default=[], doc="Competencies")
    job_description = param.String(default='', doc="Job Description")
    selected_jobs = param.List(default=[], doc="Selected Jobs")
    selected_projects = param.List(default=[], doc="Selected Projects")
    selected_competencies = param.List(default=[], doc="Selected Competencies")

    def __init__(self, **params):
        super().__init__(**params)
        self.project_editor = JSONEditor(value=[project.dict() for project in self.projects], mode="tree")
        self.jobs_editor = JSONEditor(value=[job.dict() for job in self.jobs], mode="tree")

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(
            "### Step 3: Select Content",
            self.jobs_editor,
            self.project_editor
        )

    @param.output(selected_projects=param.List, selected_jobs=param.List, selected_competencies=param.List)
    def output(self):
        project_names = [p["name"] for p in self.project_editor.value]
        job_company = [j["company"] for j in self.jobs_editor.value]  # TODO company name is not unique. fix this
        self.selected_projects = [p for p in self.projects if p.name in project_names]
        self.selected_jobs = [j for j in self.jobs if j.company in job_company]
        return self.selected_projects, self.selected_jobs, self.selected_competencies
