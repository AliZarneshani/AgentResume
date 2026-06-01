# AgentResume

AgentResume is a **Multi-Agent Resume Analysis System** that compares a PDF resume with a job description and generates a structured hiring report.

It uses **FastAPI** as the backend, **LangGraph** for multi-agent workflow orchestration, **AvalAI** as an OpenAI-compatible LLM provider, and **Streamlit** as the user interface.

---

## Features

* PDF resume upload
* Job description analysis
* Resume parsing
* Job requirement extraction
* Resume-job matching
* Gap analysis
* Candidate scoring from `0` to `10`
* Final hiring report
* Debug endpoint for development
* Streamlit UI
* Docker Compose support

---

## Tech Stack

* Python 3.11+
* FastAPI
* LangChain
* LangGraph
* Pydantic
* AvalAI API
* pypdf
* Streamlit
* Docker

---

## Architecture

```text
Streamlit UI
    ↓
FastAPI API
    ↓
PDF Text Extractor
    ↓
LangGraph Workflow
    ↓
Resume Parser Agent
    ↓
Job Description Agent
    ↓
Match Analysis Agent
    ↓
Gap Analysis Agent
    ↓
Scoring Agent
    ↓
Final Report
```

---

## Project Structure

```text
app/
├── agents/
├── api/
├── core/
├── graph/
├── schemas/
├── services/
└── main.py

frontend/
└── streamlit_app.py

Dockerfile
Dockerfile.streamlit
docker-compose.yml
requirements.txt
README.md
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
AVALAI_API_KEY=your_avalai_api_key_here
AVALAI_BASE_URL=https://api.avalai.ir/v1
AVALAI_MODEL=gpt-4o-mini
```

---

## Installation

```bash
uv venv
uv pip install -r requirements.txt
```

Activate virtual environment on Windows:

```bash
.venv\Scripts\activate
```

---

## Run Locally

Start the FastAPI backend:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Start the Streamlit frontend in another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open the UI:

```text
http://localhost:8501
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

---

## Run with Docker

```bash
docker-compose up --build
```

Streamlit UI:

```text
http://127.0.0.1:8501
```

FastAPI docs:

```text
http://127.0.0.1:8001/docs
```

Stop containers:

```bash
docker-compose down
```

---

## API Endpoints

### `POST /analyze`

Returns the final resume analysis report.

Inputs:

| Field             | Type   | Description          |
| ----------------- | ------ | -------------------- |
| `job_description` | string | Job description text |
| `resume_file`     | file   | PDF resume           |

Example response:

```json
{
  "overall_score": 6.5,
  "strengths_summary": [
    "Strong Python background"
  ],
  "weaknesses_summary": [
    "Limited frontend experience"
  ],
  "gaps_found": [
    "Moderate: PostgreSQL experience is not clearly shown"
  ],
  "recommendations": [
    "Add more backend API projects to the resume"
  ],
  "hiring_recommendation": "Consider",
  "confidence_level": "Medium",
  "detailed_analysis": "Candidate is a partial match for the role."
}
```

### `POST /analyze/debug`

Returns the full internal workflow output:

* Extracted resume text
* Parsed resume
* Parsed job description
* Match analysis
* Gap analysis
* Scoring analysis
* Final report

---

## Current Limitations

* Only PDF resumes are supported
* Scanned PDFs are not supported yet
* No authentication
* No database
* No caching
* Final report consistency can still be improved

---

## Roadmap

* Add Final Report Agent
* Add OCR support
* Add authentication
* Add database storage
* Add batch resume analysis
* Add downloadable report
* Improve Streamlit UI

---

## Author

Developed by Ali Zarneshani.
