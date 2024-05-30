import panel as pn
from .pages import Step1, Step2, Step3, Step4


class CVBuilderApp:
    def __init__(self):
        self.pipeline = pn.pipeline.Pipeline(stages=[
            ('Step 1: Fill Information', Step1),
            # ('Step 2: Fetch Information', Step2),
            # ('Step 3: Select Content', Step3),
            ('Step 4: Build and Review', Step4),
        ])

    def servable(self):
        return self.pipeline


if __name__.startswith('bokeh'):
    app = CVBuilderApp()
    app.servable().servable()

if __name__ == '__main__':
    app = CVBuilderApp()
    app.servable().show()
