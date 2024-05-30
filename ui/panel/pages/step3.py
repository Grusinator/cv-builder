import param
import panel as pn
from panel.widgets import TextAreaInput


class Step3(param.Parameterized):
    fetch_status = param.String(default='', doc="Fetch Status")
    selected_content = param.String(default='', doc="Selected Content")

    def panel(self):
        return pn.Row(self.view)

    def view(self):
        return pn.Column(
            "### Step 3: Select Content",
            TextAreaInput(name='Select Content', value=self.selected_content, height=100),
        )

    @param.output(('selected_content', param.String))
    def output(self):
        return self.selected_content
