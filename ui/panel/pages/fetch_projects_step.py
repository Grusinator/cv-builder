import param
import panel as pn
from panel.widgets import TextAreaInput, Button, JSONEditor

from cv_compiler.cv_builder import CVCompiler
from cv_compiler.models import GithubProject


class FetchProjectsStep(param.Parameterized):
    job_description = param.String(default="", doc="Job Description")
    projects = param.List(default=[], doc="Projects")

    github_username = param.String(default='', doc="GitHub Username")
    github_token = param.String(default='', doc="github token")
    fetch_status = param.String(default='', doc="Fetch Status")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVCompiler()
        self.projects_editor = JSONEditor(value=[proj.dict() for proj in self.projects], mode="tree")

    def panel(self):
        return self.view()

    @param.depends("projects", "job_description", "github_username", "github_token")
    def view(self):
        return pn.Column(
            "### Step 2: Fetch Information from Providers",
            TextAreaInput(name='GitHub Username', value=self.github_username, height=50),
            TextAreaInput(name='Github token', value=self.github_token, height=50),
            Button(name='Fetch Github Projects', button_type='primary', on_click=self.fetch_github_projects),
            self.fetch_status,
            self.projects_editor
        )

    def fetch_github_projects(self, event):
        self.fetch_status = "Fetching GitHub projects...  Please wait"
        self.projects = self.cv_compiler.fetch_github_projects(self.github_username, self.github_token)
        self.fetch_status = "Fetch complete!"
        self.projects_editor.value = [proj.dict() for proj in self.projects]

    @param.output(projects=param.List)
    def output(self):
        self.projects = [GithubProject(**p) for p in self.projects_editor.value]
        return self.projects
