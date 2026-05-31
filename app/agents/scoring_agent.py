import json

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.analysis import GapAnalysis, MatchAnalysis, ScoringAnalysis
from app.schemas.job import ParsedJobDescription
from app.schemas.resume import ParsedResume
from app.services.llm_client import get_llm


def score_candidate(
    parsed_resume: ParsedResume,
    parsed_job: ParsedJobDescription,
    match_analysis: MatchAnalysis,
    gap_analysis: GapAnalysis,
) -> ScoringAnalysis:
    parser = PydanticOutputParser(pydantic_object=ScoringAnalysis)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert HR scoring specialist.

Your job is to assign a fair candidate-job match score from 0 to 10.

Scoring rules:
- overall_score must be between 0 and 10.
- score_breakdown fields must also be between 0 and 10.
- Be evidence-based.
- Do not invent candidate skills or experience.
- Penalize critical gaps more than moderate or minor gaps.
- Consider required skills more important than preferred skills.
- Consider experience requirements, education, tools, and overall fit.
- Return only valid JSON.
- Do not add explanations outside JSON.
- Keep the output compatible with the provided schema.

Hiring recommendation should be one of:
- Strong Hire
- Hire
- Consider
- Weak Consider
- Reject

Confidence level should be one of:
- High
- Medium
- Low

{format_instructions}
""",
            ),
            (
                "human",
                """
Parsed resume JSON:
{parsed_resume}

Parsed job description JSON:
{parsed_job}

Match analysis JSON:
{match_analysis}

Gap analysis JSON:
{gap_analysis}
""",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | get_llm() | parser

    return chain.invoke(
        {
            "parsed_resume": json.dumps(
                parsed_resume.model_dump(),
                ensure_ascii=False,
                indent=2,
            ),
            "parsed_job": json.dumps(
                parsed_job.model_dump(),
                ensure_ascii=False,
                indent=2,
            ),
            "match_analysis": json.dumps(
                match_analysis.model_dump(),
                ensure_ascii=False,
                indent=2,
            ),
            "gap_analysis": json.dumps(
                gap_analysis.model_dump(),
                ensure_ascii=False,
                indent=2,
            ),
        }
    )