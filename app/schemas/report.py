from pydantic import BaseModel, Field

from app.schemas.analysis import ScoreBreakdown


class FinalReport(BaseModel):
    overall_score: float = 0.0
    score_breakdown: ScoreBreakdown = Field(default_factory=ScoreBreakdown)

    strengths_summary: list[str] = Field(default_factory=list)
    weaknesses_summary: list[str] = Field(default_factory=list)
    gaps_found: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

    hiring_recommendation: str = ""
    confidence_level: str = ""

    detailed_analysis: str = ""