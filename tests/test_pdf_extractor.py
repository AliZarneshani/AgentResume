from app.services.pdf_extractor import extract_text_from_pdf


def test_pdf_extractor():
    text = extract_text_from_pdf("sample_resume.pdf")

    assert len(text) > 0