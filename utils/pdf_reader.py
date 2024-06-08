import io

import pdfplumber


class PdfReader:

    def extract_text_from_pdf(self, pdf_bytes: bytes):
        text = ''
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() if page.extract_text() else ''
        return text