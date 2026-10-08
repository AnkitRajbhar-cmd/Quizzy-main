from pypdf import PdfReader
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text
