from .cleaner import clean_text
from .extractor import extract_pdf_text


def process_pdf (pdf_path: str) -> str:
    raw = extract_pdf_text(pdf_path)
    cleaned_text = clean_text(raw)
    return cleaned_text

