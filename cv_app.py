from dotenv import load_dotenv

from ui.panel.app import CVBuilderApp

load_dotenv()

if __name__.startswith('bokeh'):
    app = CVBuilderApp()
    app.servable().servable()

if __name__ == '__main__':
    app = CVBuilderApp()
    app.servable().show()