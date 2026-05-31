from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm():
    return ChatOpenAI(
        api_key=settings.AVALAI_API_KEY,
        base_url=settings.AVALAI_BASE_URL,
        model=settings.AVALAI_MODEL,
        temperature=0,
    )