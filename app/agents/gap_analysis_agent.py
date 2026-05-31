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
- Use semantic evidence, not only exact keyword matching.
- Do not mark a requirement as a critical gap if the resume contains strong equivalent experience.
- If a requirement is partially covered, classify it as moderate or minor, not critical.
- Critical gaps should be reserved for essential requirements with little or no evidence in the resume.
- A moderate gap is important but partially covered or learnable.
- A minor gap is useful to improve but not a major concern.
- For every gap, provide a practical suggestion.
- Use the parsed resume, parsed job description, and match analysis as evidence.
- Keep the output compatible with the provided schema.

Examples:
- If the job requires API design and the resume has FastAPI, backend, or REST-related experience, this is not a critical gap.
- If the job requires AI tools and the resume has LLM, RAG, LangChain, LangGraph, or AI engineering experience, this is not a critical gap.
- If the job requires a specific database such as PostgreSQL but the resume only has SQL, this is a moderate gap, not a complete missing skill.

{format_instructions}
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