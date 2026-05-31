from langgraph.graph import END, StateGraph

from app.graph.nodes import (
    final_report_node,
    gap_analysis_node,
    match_analysis_node,
    parse_job_node,
    parse_resume_node,
    scoring_node,
)
from app.graph.state import ResumeAnalysisState


def build_resume_analysis_workflow():
    workflow = StateGraph(ResumeAnalysisState)

    workflow.add_node("parse_resume", parse_resume_node)
    workflow.add_node("parse_job", parse_job_node)
    workflow.add_node("match_analysis", match_analysis_node)
    workflow.add_node("gap_analysis", gap_analysis_node)
    workflow.add_node("scoring", scoring_node)
    workflow.add_node("final_report", final_report_node)

    workflow.set_entry_point("parse_resume")

    workflow.add_edge("parse_resume", "parse_job")
    workflow.add_edge("parse_job", "match_analysis")
    workflow.add_edge("match_analysis", "gap_analysis")
    workflow.add_edge("gap_analysis", "scoring")
    workflow.add_edge("scoring", "final_report")
    workflow.add_edge("final_report", END)

    return workflow.compile()


resume_analysis_workflow = build_resume_analysis_workflow()