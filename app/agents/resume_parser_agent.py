from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.resume import ParsedResume
from app.services.llm_client import get_llm


def parse_resume(resume_text: str) -> ParsedResume:
    parser = PydanticOutputParser(pydantic_object=ParsedResume)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert resume parser.

Extract structured information from the resume text.

Rules:
- Return only valid JSON.
- Do not add explanations.
- If a field is missing, use an empty string, empty list, or 0.
- Keep the output compatible with the provided schema.

{format_instructions}
""",
            ),
            (
                "human",
                """
Resume text:

{resume_text}
""",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | get_llm() | parser

    return chain.invoke({"resume_text": resume_text})