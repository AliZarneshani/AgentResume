from pydantic import BaseModel, Field


class MatchAnalysis(BaseModel):
    matched_required_skills: list[str] = Field(default_factory=list)
    matched_preferred_skills: list[str] = Field(default_factory=list)
    missing_required_skills: list[str] = Field(default_factory=list)
    missing_preferred_skills: list[str] = Field(default_factory=list)

    experience_match: str = ""
    education_match: str = ""

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    overall_match_summary: str = ""


class GapItem(BaseModel):
    requirement: str = ""
    gap_type: str = ""
    severity: str = ""
    evidence: str = ""
    suggestion: str = ""


class GapAnalysis(BaseModel):
    critical_gaps: list[GapItem] = Field(default_factory=list)
    moderate_gaps: list[GapItem] = Field(default_factory=list)
    minor_gaps: list[GapItem] = Field(default_factory=list)

    risk_level: str = ""
    risk_summary: str = ""

    improvement_recommendations: list[str] = Field(default_factory=list)
    overall_gap_summary: str = ""