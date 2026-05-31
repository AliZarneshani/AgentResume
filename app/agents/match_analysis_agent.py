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
- Use semantic matching, not only exact keyword matching.
- If the resume shows equivalent or closely related experience, count it as a match or partial match.
- For example:
  - FastAPI experience can support API design/backend development.
  - SQL can partially support database experience, even if PostgreSQL/MySQL is not explicitly listed.
  - LLM, RAG, LangChain, LangGraph, AI engineering, or model fine-tuning can support AI-tool or AI-assisted development requirements.
  - Python backend experience can partially support backend development.
- If a requirement is only partially covered, do not mark it as a full strength; mention the limitation in weaknesses.
- Required skills are more important than preferred skills.
- If something is not clearly present or semantically supported by the resume, treat it as missing.
- Keep the output compatible with the provided schema.

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
        }
    )