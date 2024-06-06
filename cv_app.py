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
    user_id = doc.session_context.request.arguments.get('user_id', [""])[0]

    # Store the user ID in pn.state for access throughout the session
    pn.state.user_id = user_id
    _app = CVBuilderApp().view()
    _app.server_doc(doc)
