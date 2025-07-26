# from pypdf import PdfReader

# def extract_pdf_text(pdf_path: str) -> str:

#     reader = PdfReader(pdf_path)
#     text = ""

#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
            
    
#     return text

import fitz  # PyMuPDF

def extract_pdf_text(pdf_path: str) -> str:
    reader = fitz.open(pdf_path)  # using the same variable name: 'reader'
    text = ""

    for page in reader:  # reader acts like an iterable of pages
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    return text
