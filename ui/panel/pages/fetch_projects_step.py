import param
import panel as pn
from panel.widgets import TextAreaInput, Button

from cv_compiler.cv_builder import CVCompiler


class FetchProjectsStep(param.Parameterized):
    info_text = param.String(default='', doc="Personal Information")
    job_description = param.String(default='', doc="Job Description")
    github_username = param.String(default='', doc="GitHub Username")
    github_token = param.String(default='', doc="github token")
    fetch_status = param.String(default='', doc="Fetch Status")
    projects = param.List(default=[], doc="Projects")

    def __init__(self, **params):
        super().__init__(**params)
        self.cv_compiler = CVCompiler()
        self.save_button = Button(name='Select Projects', button_type='primary', on_click=self.select_projects)
        self.cross_selector = pn.widgets.CrossSelector(name='Projects', value=[],
                                                       options=[proj.name for proj in self.projects])

    def panel(self):
        return self.view()

    @param.depends("projects", "job_description", "github_username", "github_token")
    def view(self):
        return pn.Column(
            "### Step 2: Fetch Information from Providers",
            TextAreaInput(name='GitHub Username', value=self.github_username, height=50),
            TextAreaInput(name='Github token', value=self.github_token, height=50),
            Button(name='Fetch Info', button_type='primary', on_click=self.fetch_info),
            self.cross_selector,
            self.save_button
        )

    def fetch_info(self, event):
        self.projects = self.cv_compiler.fetch_github_projects(self.github_username, self.github_token)
        self.fetch_status = "Fetched GitHub"

    def select_projects(self, event):
        selected_projects = [proj for proj in self.projects if proj.name in self.cross_selector.value]
        self.cv_compiler.update_generated_projects(selected_projects)

    @param.output(projects=param.List)
    def output(self):
        return self.projects
