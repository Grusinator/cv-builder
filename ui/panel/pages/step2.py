import param
import panel as pn
from panel.widgets import TextAreaInput, Button

class Step2(param.Parameterized):
    info_text = param.String(default='', doc="Personal Information")
    job_description = param.String(default='', doc="Job Description")
    github_username = param.String(default='', doc="GitHub Username")
    linkedin_url = param.String(default='', doc="LinkedIn URL")
    fetch_status = param.String(default='', doc="Fetch Status")

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(
            "### Step 2: Fetch Information from Providers",
            TextAreaInput(name='GitHub Username', value=self.github_username, height=50),
            TextAreaInput(name='LinkedIn URL', value=self.linkedin_url, height=50),
            Button(name='Fetch Info', button_type='primary', on_click=self.fetch_info),
            pn.pane.Markdown(self.fetch_status)
        )

    def fetch_info(self, event):
        self.fetch_status = "Fetched GitHub and LinkedIn info."

    @param.output(('github_username', param.String), ('linkedin_url', param.String), ('fetch_status', param.String))
    def output(self):
        return self.github_username, self.linkedin_url, self.fetch_status
