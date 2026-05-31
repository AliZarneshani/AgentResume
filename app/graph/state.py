from typing import TypedDict

from app.schemas.analysis import GapAnalysis, MatchAnalysis, ScoringAnalysis
from app.schemas.job import ParsedJobDescription
from app.schemas.report import FinalReport
from app.schemas.resume import ParsedResume


class ResumeAnalysisState(TypedDict, total=False):
    job_description: str
    resume_text: str

    parsed_resume: ParsedResume
    parsed_job: ParsedJobDescription

    match_analysis: MatchAnalysis
    gap_analysis: GapAnalysis
    scoring_analysis: ScoringAnalysis

    final_report: FinalReport