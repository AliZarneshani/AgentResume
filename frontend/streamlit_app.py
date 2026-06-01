import os

import requests
import streamlit as st


DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="AgentResume",
    page_icon="📄",
    layout="wide",
)


st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        .main .block-container {
            max-width: 1100px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        .hero {
            text-align: center;
            padding: 1.5rem 0 2rem 0;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .hero-subtitle {
            color: #6b7280;
            font-size: 1.05rem;
        }

        .section-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 1.5rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.5rem;
        }

        .score-box {
            background: linear-gradient(135deg, #111827, #1f2937);
            color: white;
            border-radius: 22px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .score-number {
            font-size: 4rem;
            font-weight: 900;
            line-height: 1;
            margin: 0.7rem 0;
        }

        .score-meta {
            color: #d1d5db;
            font-size: 1rem;
            margin-top: 0.3rem;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.95rem;
        }

        div.stButton > button {
            height: 3rem;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


api_url = DEFAULT_API_URL
use_debug_endpoint = False


st.markdown(
    """
    <div class="hero">
        <div class="hero-title">📄 AgentResume</div>
        <div class="hero-subtitle">
            Multi-Agent Resume Analysis powered by FastAPI, LangGraph, and AvalAI
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.expander("Advanced Settings", expanded=False):
    api_url = st.text_input(
        "FastAPI URL",
        value=DEFAULT_API_URL,
        help="Use http://127.0.0.1:8000 locally or http://api:8000 inside Docker Compose.",
    )

    use_debug_endpoint = st.checkbox(
        "Use debug endpoint",
        value=False,
        help="Shows internal outputs such as parsed resume, parsed job, match analysis, and gap analysis.",
    )

    endpoint_preview = "/analyze/debug" if use_debug_endpoint else "/analyze"
    st.caption("Current endpoint")
    st.code(f"{api_url.rstrip('/')}{endpoint_preview}")


st.markdown("## Upload Resume and Job Description")

job_description = st.text_area(
    "Job Description",
    height=260,
    placeholder="Paste the job description here...",
)

resume_file = st.file_uploader(
    "Resume PDF",
    type=["pdf"],
)

analyze_button = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True,
)


def render_list(title: str, items: list[str]) -> None:
    st.subheader(title)

    if not items:
        st.info("No items found.")
        return

    for item in items:
        st.markdown(f"- {item}")


def render_score_breakdown(score_breakdown: dict) -> None:
    st.subheader("Score Breakdown")

    labels = {
        "skills_score": "Skills",
        "experience_score": "Experience",
        "education_score": "Education",
        "tools_score": "Tools",
        "overall_fit_score": "Overall Fit",
    }

    for key, label in labels.items():
        value = float(score_breakdown.get(key, 0) or 0)
        st.write(f"**{label}:** {value}/10")
        st.progress(min(max(value / 10, 0), 1))


def render_final_report(report: dict) -> None:
    overall_score = float(report.get("overall_score", 0) or 0)

    st.markdown("---")
    st.markdown("## Final Report")

    st.markdown(
        f"""
        <div class="score-box">
            <div class="small-muted">Overall Score</div>
            <div class="score-number">{overall_score}/10</div>
            <div class="score-meta">
                Recommendation: {report.get("hiring_recommendation", "N/A")}
            </div>
            <div class="score-meta">
                Confidence: {report.get("confidence_level", "N/A")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(min(max(overall_score / 10, 0), 1))

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            render_score_breakdown(report.get("score_breakdown", {}))

    with col2:
        with st.container(border=True):
            render_list("Strengths", report.get("strengths_summary", []))

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            render_list("Weaknesses", report.get("weaknesses_summary", []))

    with col4:
        with st.container(border=True):
            render_list("Recommendations", report.get("recommendations", []))

    with st.container(border=True):
        render_list("Gaps Found", report.get("gaps_found", []))

    with st.container(border=True):
        st.subheader("Detailed Analysis")
        st.write(report.get("detailed_analysis", "No detailed analysis available."))


def render_debug_output(data: dict) -> None:
    final_report = data.get("final_report", {})

    render_final_report(final_report)

    st.markdown("---")
    st.markdown("## Debug Output")

    with st.expander("Extracted Resume Text"):
        st.text(data.get("resume_text", ""))

    with st.expander("Parsed Resume JSON"):
        st.json(data.get("parsed_resume", {}))

    with st.expander("Parsed Job JSON"):
        st.json(data.get("parsed_job", {}))

    with st.expander("Match Analysis JSON"):
        st.json(data.get("match_analysis", {}))

    with st.expander("Gap Analysis JSON"):
        st.json(data.get("gap_analysis", {}))

    with st.expander("Scoring Analysis JSON"):
        st.json(data.get("scoring_analysis", {}))

    with st.expander("Final Report JSON"):
        st.json(final_report)


if analyze_button:
    if not job_description.strip():
        st.error("Job description cannot be empty.")
        st.stop()

    if resume_file is None:
        st.error("Please upload a PDF resume.")
        st.stop()

    endpoint = "/analyze/debug" if use_debug_endpoint else "/analyze"
    url = f"{api_url.rstrip('/')}{endpoint}"

    files = {
        "resume_file": (
            resume_file.name,
            resume_file.getvalue(),
            "application/pdf",
        )
    }

    data = {
        "job_description": job_description,
    }

    with st.spinner("Analyzing resume... This may take a few moments."):
        try:
            response = requests.post(
                url,
                data=data,
                files=files,
                timeout=180,
            )

            response_data = response.json()

            if not response.ok:
                detail = response_data.get("detail", "Analysis failed.")
                st.error(detail)
                st.stop()

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. Make sure the API server is running."
            )
            st.stop()

        except requests.exceptions.Timeout:
            st.error("Request timed out. Try again or use a faster model.")
            st.stop()

        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
            st.stop()

    if use_debug_endpoint:
        render_debug_output(response_data)
    else:
        render_final_report(response_data)