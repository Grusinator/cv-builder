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

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(

            "### Step 3: Select Content",
            JSONEditor(value=[project.dict() for project in self.projects], mode="tree"),
            JSONEditor(value=[job.dict() for job in self.jobs], mode="tree"),
        )

    @param.output(selected_projects=param.List, selected_jobs=param.List, selected_competencies=param.List)
    def output(self):
        # TODO implement logic to select projects, jobs and competencies from json editors
        return self.selected_projects, self.selected_jobs, self.selected_competencies
