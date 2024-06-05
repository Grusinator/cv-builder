import panel as pn
from dotenv import load_dotenv

from ui.panel.app import CVBuilderApp

load_dotenv()

if __name__.startswith('bokeh'):
    app = CVBuilderApp()
    app.view().servable()

if __name__ == '__main__':
    app = CVBuilderApp()
    app.view().show()


def app(doc):
    """This function is necessary for the app to be served by Django."""
    sw = CVBuilderApp()
    row = pn.Row(sw.view())
    row.server_doc(doc)
