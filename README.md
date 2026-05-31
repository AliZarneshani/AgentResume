# AgentResume

AgentResume is a **Multi-Agent Resume Analysis API** that compares a candidate resume against a job description and generates a structured hiring report.

The system extracts text from a PDF resume, parses the resume, analyzes the job description, compares both sides, identifies gaps, assigns a score from `0` to `10`, and returns a final JSON report.

---

## Features

* PDF resume upload
* Job description input as plain text
* Resume text extraction from PDF
* Structured resume parsing
* Structured job description parsing
* Resume-job match analysis
* Gap analysis
* Candidate scoring from `0` to `10`
* Final JSON hiring report
* Debug endpoint for development
* Docker support

---

## Tech Stack

* Python 3.11+
* FastAPI
* LangChain
* LangGraph
* Pydantic
* pypdf
* Docker
* Docker Compose

---

## Architecture

```text
Client
  |
  v
FastAPI API
  |
  v
PDF Text Extractor
  |
  v
LangGraph Workflow
  |
  +--> Resume Parser Agent
  |
  +--> Job Description Parser Agent
  |
  +--> Match Analysis Agent
  |
  +--> Gap Analysis Agent
  |
  +--> Scoring Agent
  |
  v
Final Report Builder
  |
  v
JSON Response
```

---

## Project Structure

```text
app/
├── agents/
│   ├── gap_analysis_agent.py
│   ├── job_description_agent.py
│   ├── match_analysis_agent.py
│   ├── resume_parser_agent.py
│   ├── scoring_agent.py
│   └── prompts/
├── api/
│   └── routes/
│       └── analyze.py
├── core/
│   ├── config.py
│   ├── exceptions.py
│   └── logging.py
├── graph/
│   ├── nodes.py
│   ├── state.py
│   └── workflow.py
├── schemas/
│   ├── analysis.py
│   ├── job.py
│   ├── report.py
│   └── resume.py
├── services/
│   ├── llm_client.py
│   ├── pdf_extractor.py
│   ├── report_builder.py
│   └── validators.py
└── utils/
    └── json_utils.py
```

---

## Installation

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Required packages:

```txt
fastapi
uvicorn
python-multipart
pydantic
pydantic-settings
python-dotenv
langchain
langchain-openai
langgraph
pypdf
pytest
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
AVALAI_API_KEY=your_avalai_api_key_here
AVALAI_BASE_URL=https://api.avalai.ir/v1
AVALAI_MODEL=gpt-4o-mini
```

AgentResume uses AvalAI as an OpenAI-compatible provider.

You can change the model name based on the models available in your AvalAI account.

---

## Run Locally

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "AgentResume API is running"
}
```

---

## API Endpoints

### POST `/analyze`

Returns the final user-facing resume analysis report.

#### Request

Form data:

| Field             | Type   | Required | Description          |
| ----------------- | ------ | -------: | -------------------- |
| `job_description` | string |      Yes | Job description text |
| `resume_file`     | file   |      Yes | PDF resume           |

#### Example cURL

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "job_description=We are looking for a Python backend developer with FastAPI, Docker, PostgreSQL and API design experience." \
  -F "resume_file=@resume.pdf;type=application/pdf"
```

### POST `/analyze/debug`

Returns the full internal workflow output for development and debugging.

This endpoint includes:

* Extracted resume text
* Parsed resume
* Parsed job description
* Match analysis
* Gap analysis
* Scoring analysis
* Final report

Use this endpoint during development to inspect how each agent is performing.

---

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Stop containers:

```bash
docker compose down
```

---

## Validation Rules

The API currently validates:

* Only PDF files are accepted
* Empty PDF files are rejected
* PDF file size must be under the configured limit
* Job description cannot be empty
* Very short job descriptions are rejected
* Scanned or image-based PDFs may fail if no text can be extracted

---

## Current Limitations

* Only PDF resumes are supported
* Scanned PDFs are not supported yet
* No database storage
* No authentication
* No caching
* No background job queue
* LLM output quality depends on the selected AvalAI model
* The system is currently optimized for MVP usage, not high-scale production traffic

---

## Roadmap

* Add OCR fallback for scanned PDFs
* Add authentication
* Add Redis caching
* Add database support for analysis history
* Add batch resume analysis
* Add web dashboard
* Add more robust evaluation tests
* Add async/background processing
* Add configurable scoring weights
* Add support for DOCX resumes

---

## Development Notes

The main workflow is defined in:

```text
app/graph/workflow.py
```

Workflow nodes are defined in:

```text
app/graph/nodes.py
```

The final report is built in:

```text
app/services/report_builder.py
```

The main API route is defined in:

```text
app/api/routes/analyze.py
```


