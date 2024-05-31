import param
import panel as pn
from panel.widgets import TextAreaInput


class ReviewContentStep(param.Parameterized):

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
