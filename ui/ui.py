import threading
import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from cv_compiler.cv_builder import CVCompiler


class UI:

    def __init__(self, cv_builder: CVCompiler):
        self.cv_builder = cv_builder
        self.app = dash.Dash(__name__)

        self.app.layout = html.Div([
            html.Button('Build', id='build-button', n_clicks=0),
            html.Div(id='output-container-button'),
            html.Iframe(id='pdf-viewer', style={'display': 'none', 'width': '100%', 'height': '800px'})
        ])

        @self.app.callback(
            Output('output-container-button', 'children'),
            Output('pdf-viewer', 'style'),
            Input('build-button', 'n_clicks'),
            State('pdf-viewer', 'style')
        )
        def update_output(n_clicks, pdf_viewer_style):
            if n_clicks > 0:
                # threading.Thread(target=self.cv_builder.build_cv).start()
                return 'Build triggered!', {'display': 'none'}
            else:
                if os.path.exists(self.cv_builder.output_pdf_path):
                    pdf_viewer_src = f"/pdf_viewer?value={os.path.basename(self.cv_builder.output_pdf_path)}"
                    return '', {'display': 'block', 'src': pdf_viewer_src}
                else:
                    return 'Click the button to trigger the build.', {'display': 'none'}

        @self.app.server.route('/pdf_viewer')
        def serve_pdf():
            pdf_file = os.path.join(os.getcwd(), self.cv_builder.output_pdf_path)
            return dcc.send_file(pdf_file)


if __name__ == '__main__':
    _cv_builder = CVCompiler()
    ui = UI(_cv_builder)
    ui.app.run_server(debug=True, use_reloader=True, port=8050)
