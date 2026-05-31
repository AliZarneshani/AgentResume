from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.job import ParsedJobDescription
from app.services.llm_client import get_llm


def parse_job_description(job_description: str) -> ParsedJobDescription:
    parser = PydanticOutputParser(pydantic_object=ParsedJobDescription)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert HR job description analyzer.

Extract structured hiring requirements from the job description.

Rules:
- Return only valid JSON.
- Do not add explanations.
- If a field is missing, use an empty string, empty list, or 0.
- Keep the output compatible with the provided schema.
- Separate required skills from preferred skills if possible.
- Extract tools, technologies, responsibilities, seniority level, and experience requirements.

{format_instructions}
""",
            ),
            (
                "human",
                """
Job description:

{job_description}
""",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | get_llm() | parser

    return chain.invoke({"job_description": job_description})