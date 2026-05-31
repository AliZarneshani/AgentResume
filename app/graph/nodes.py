from app.agents.gap_analysis_agent import analyze_gaps
from app.agents.job_description_agent import parse_job_description
from app.agents.match_analysis_agent import analyze_match
from app.agents.resume_parser_agent import parse_resume
from app.agents.scoring_agent import score_candidate
from app.graph.state import ResumeAnalysisState
from app.services.report_builder import build_final_report


def parse_resume_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    parsed_resume = parse_resume(state["resume_text"])

    return {
        "parsed_resume": parsed_resume,
    }


def parse_job_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    parsed_job = parse_job_description(state["job_description"])

    return {
        "parsed_job": parsed_job,
    }


def match_analysis_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    match_analysis = analyze_match(
        parsed_resume=state["parsed_resume"],
        parsed_job=state["parsed_job"],
    )

    return {
        "match_analysis": match_analysis,
    }


def gap_analysis_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    gap_analysis = analyze_gaps(
        parsed_resume=state["parsed_resume"],
        parsed_job=state["parsed_job"],
        match_analysis=state["match_analysis"],
    )

    return {
        "gap_analysis": gap_analysis,
    }


def scoring_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    scoring_analysis = score_candidate(
        parsed_resume=state["parsed_resume"],
        parsed_job=state["parsed_job"],
        match_analysis=state["match_analysis"],
        gap_analysis=state["gap_analysis"],
    )

    return {
        "scoring_analysis": scoring_analysis,
    }


def final_report_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    final_report = build_final_report(
        match_analysis=state["match_analysis"],
        gap_analysis=state["gap_analysis"],
        scoring_analysis=state["scoring_analysis"],
    )

    return {
        "final_report": final_report,
    }