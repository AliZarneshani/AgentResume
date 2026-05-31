from pydantic import BaseModel, Field


class ParsedJobDescription(BaseModel):
    job_title: str = ""
    seniority_level: str = ""

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)

    required_experience_years: float = 0.0
    education_requirements: list[str] = Field(default_factory=list)

    tools_and_technologies: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)

    keywords: list[str] = Field(default_factory=list)