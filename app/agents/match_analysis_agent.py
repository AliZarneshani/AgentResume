import json

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.analysis import MatchAnalysis
from app.schemas.job import ParsedJobDescription
from app.schemas.resume import ParsedResume
from app.services.llm_client import get_llm


def analyze_match(
    parsed_resume: ParsedResume,
    parsed_job: ParsedJobDescription,
) -> MatchAnalysis:
    parser = PydanticOutputParser(pydantic_object=MatchAnalysis)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert HR resume-job matching analyst.

Compare the parsed resume against the parsed job description.

Rules:
- Return only valid JSON.
- Do not add explanations outside JSON.
- Be fair and evidence-based.
- Do not invent skills or experience.
- If something is not clearly present in the resume, treat it as missing.
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
        }
    )