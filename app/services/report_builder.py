from app.schemas.analysis import GapAnalysis, MatchAnalysis, ScoringAnalysis
from app.schemas.report import FinalReport


def build_final_report(
    match_analysis: MatchAnalysis,
    gap_analysis: GapAnalysis,
    scoring_analysis: ScoringAnalysis,
) -> FinalReport:
    gaps_found: list[str] = []

    for gap in gap_analysis.critical_gaps:
        gaps_found.append(f"Critical: {gap.requirement} - {gap.suggestion}")

    for gap in gap_analysis.moderate_gaps:
        gaps_found.append(f"Moderate: {gap.requirement} - {gap.suggestion}")

    for gap in gap_analysis.minor_gaps:
        gaps_found.append(f"Minor: {gap.requirement} - {gap.suggestion}")

    detailed_analysis = (
        f"{match_analysis.overall_match_summary}\n\n"
        f"Gap Summary: {gap_analysis.overall_gap_summary}\n\n"
        f"Risk Level: {gap_analysis.risk_level}\n"
        f"Risk Summary: {gap_analysis.risk_summary}\n\n"
        f"Score Reasoning: {scoring_analysis.score_reasoning}"
    )

    return FinalReport(
        overall_score=scoring_analysis.overall_score,
        score_breakdown=scoring_analysis.score_breakdown,
        strengths_summary=match_analysis.strengths,
        weaknesses_summary=match_analysis.weaknesses,
        gaps_found=gaps_found,
        recommendations=gap_analysis.improvement_recommendations,
        hiring_recommendation=scoring_analysis.hiring_recommendation,
        confidence_level=scoring_analysis.confidence_level,
        detailed_analysis=detailed_analysis,
    )