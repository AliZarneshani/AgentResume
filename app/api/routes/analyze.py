import os
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.graph.workflow import resume_analysis_workflow
from app.schemas.report import FinalReport
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.validators import validate_job_description, validate_pdf_file

router = APIRouter()


async def extract_resume_text_from_upload(resume_file: UploadFile) -> str:
    content = await validate_pdf_file(resume_file)

    temp_path = ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        resume_text = extract_text_from_pdf(temp_path)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF. The PDF may be scanned or image-based.",
        )

    return resume_text


def run_resume_analysis(job_description: str, resume_text: str) -> dict:
    try:
        return resume_analysis_workflow.invoke(
            {
                "job_description": job_description,
                "resume_text": resume_text,
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(exc)}",
        ) from exc


@router.post("/analyze", response_model=FinalReport)
async def analyze_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    validate_job_description(job_description)

    resume_text = await extract_resume_text_from_upload(resume_file)

    result = run_resume_analysis(
        job_description=job_description,
        resume_text=resume_text,
    )

    return result["final_report"]


@router.post("/analyze/debug")
async def analyze_resume_debug(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    validate_job_description(job_description)

    resume_text = await extract_resume_text_from_upload(resume_file)

    result = run_resume_analysis(
        job_description=job_description,
        resume_text=resume_text,
    )

    return {
        "resume_text": resume_text,
        "parsed_resume": result["parsed_resume"].model_dump(),
        "parsed_job": result["parsed_job"].model_dump(),
        "match_analysis": result["match_analysis"].model_dump(),
        "gap_analysis": result["gap_analysis"].model_dump(),
        "scoring_analysis": result["scoring_analysis"].model_dump(),
        "final_report": result["final_report"].model_dump(),
    }