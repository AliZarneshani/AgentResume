import os
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.agents.gap_analysis_agent import analyze_gaps
from app.agents.job_description_agent import parse_job_description
from app.agents.match_analysis_agent import analyze_match
from app.agents.resume_parser_agent import parse_resume
from app.services.pdf_extractor import extract_text_from_pdf

router = APIRouter()


@router.post("/analyze")
async def analyze_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        content = await resume_file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        resume_text = extract_text_from_pdf(temp_path)
    finally:
        os.remove(temp_path)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    parsed_resume = parse_resume(resume_text)
    parsed_job = parse_job_description(job_description)
    match_analysis = analyze_match(parsed_resume, parsed_job)
    gap_analysis = analyze_gaps(parsed_resume, parsed_job, match_analysis)

    return {
        "parsed_resume": parsed_resume.model_dump(),
        "parsed_job": parsed_job.model_dump(),
        "match_analysis": match_analysis.model_dump(),
        "gap_analysis": gap_analysis.model_dump(),
    }