import re

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    text = "\n".join(pages)

    
    text = re.sub(r"\s+", " ", text)

    return text.strip()