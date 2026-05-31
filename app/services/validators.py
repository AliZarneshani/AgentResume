from fastapi import HTTPException, UploadFile

MAX_PDF_SIZE_MB = 5
MAX_PDF_SIZE_BYTES = MAX_PDF_SIZE_MB * 1024 * 1024


def validate_job_description(job_description: str) -> None:
    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty",
        )

    if len(job_description.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short",
        )


async def validate_pdf_file(resume_file: UploadFile) -> bytes:
    if resume_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    content = await resume_file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty",
        )

    if len(content) > MAX_PDF_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"PDF file size must be less than {MAX_PDF_SIZE_MB} MB",
        )

    return content