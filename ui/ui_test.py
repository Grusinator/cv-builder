import os
import base64
import dash
import threading
from dash import dcc, html
from dash.dependencies import Input, Output, State
from time import sleep


class CVCompiler:
    def __init__(self):
        self.output_pdf_path = 'output.pdf'

    def build_cv(self, job_application_text):
        # Simulate a long-running process
        sleep(3)  # Replace with actual CV building logic
        with open(self.output_pdf_path, 'wb') as f:
            f.write(b"%PDF-1.4\n%This is a dummy PDF file\n")


class UI:
    def __init__(self, cv_builder: CVCompiler):
        self.cv_builder = cv_builder
        self.app = dash.Dash(__name__)

        self.pdf_path = self.cv_builder.output_pdf_path
        self.pdf_data = self.read_pdf(self.pdf_path)
        self.building = False
        self.build_thread = None

        self.app.layout = html.Div([
            dcc.Textarea(
                id='job-application',
                placeholder='Enter the job application text here...',
                style={'width': '100%', 'height': '100px'}
            ),
            html.Button('Build CV', id='build-button', n_clicks=0),
            dcc.Interval(
                id='interval-component',
                interval=2 * 1000,  # in milliseconds
                n_intervals=0
            ),
            dcc.Loading(
                id='loading',
                type='default',
                children=[
                    html.Div(id='processing-status'),
                    html.Div(id='build-output'),
                    html.Iframe(
                        id='pdf-viewer',
                        src=f"data:application/pdf;base64,{self.pdf_data}",
                        style={'width': '100%', 'height': '800px'}
                    ),
                    html.A(
                        'Download PDF',
                        id='download-link',
                        download=os.path.basename(self.pdf_path),
                        href=f"data:application/pdf;base64,{self.pdf_data}",
                        target="_blank"
                    )
                ]
            )
        ])

        self.app.callback(
            [Output('pdf-viewer', 'src'), Output('download-link', 'href'), Output('build-output', 'children'),
             Output('processing-status', 'children')],
            [Input('build-button', 'n_clicks'), Input('interval-component', 'n_intervals')],
            [State('job-application', 'value')]
        )(self.build_cv)

    def read_pdf(self, pdf_path):
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        return ""

    def build_cv_job(self, job_application_text):
        self.cv_builder.build_cv(job_application_text)
        self.building = False

    def build_cv(self, n_clicks, n_intervals, job_application_text):
        if n_clicks > 0 and not self.building:
            self.building = True
            self.build_thread = threading.Thread(target=self.build_cv_job, args=(job_application_text,))
            self.build_thread.start()
            processing_status = "Processing..."
            return dash.no_update, dash.no_update, "", processing_status

        if self.building:
            return dash.no_update, dash.no_update, "", "Processing..."

        if not self.building and self.build_thread and not self.build_thread.is_alive():
            self.pdf_data = self.read_pdf(self.cv_builder.output_pdf_path)
            pdf_src = f"data:application/pdf;base64,{self.pdf_data}"
            download_href = pdf_src
            return pdf_src, download_href, "CV built successfully!", "Complete"

        return dash.no_update, dash.no_update, "", ""


if __name__ == '__main__':
    _cv_builder = CVCompiler()
    ui = UI(_cv_builder)
    ui.app.run_server(debug=True, use_reloader=True, port=8050)
