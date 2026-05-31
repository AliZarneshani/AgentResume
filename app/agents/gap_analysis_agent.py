import json

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.analysis import GapAnalysis, MatchAnalysis
from app.schemas.job import ParsedJobDescription
from app.schemas.resume import ParsedResume
from app.services.llm_client import get_llm


def analyze_gaps(
    parsed_resume: ParsedResume,
    parsed_job: ParsedJobDescription,
    match_analysis: MatchAnalysis,
) -> GapAnalysis:
    parser = PydanticOutputParser(pydantic_object=GapAnalysis)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert HR gap analysis specialist.

Your job is to identify the most important gaps between a candidate resume and a job description.

Rules:
- Return only valid JSON.
- Do not add explanations outside JSON.
- Do not invent missing information.
- Use the parsed resume, parsed job description, and match analysis as evidence.
- Classify gaps into critical, moderate, and minor.
- A critical gap is something that strongly affects the candidate's suitability.
- A moderate gap is important but not disqualifying.
- A minor gap is useful to improve but not a major concern.
- For every gap, provide a practical suggestion.
- Keep the output compatible with the provided schema.

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
        }
    )