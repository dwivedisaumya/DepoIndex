# DepoIndex

**DepoIndex** is a legal-tech application that converts structured deposition transcripts into a **chronology-first topic index** with grounded evidence and source-level traceability.

## Features

- 📄 Persis Yu deposition as the reference document
- 📤 Upload supported legal/deposition PDFs
- 🔎 Grounded testimony search
- 🧵 Topic threads and re-entry detection
- 📅 Interactive chronology timeline
- 📌 Evidence and source-line navigation
- 🔐 Provenance and integrity checks
- 👩‍⚖️ Human review support
- 📊 JSON and Markdown exports

## How It Works

```text
PDF
 ↓
Canonical Transcript
 ↓
Topic Detection
 ↓
Evidence Validation
 ↓
Topic Threads & Timeline
 ↓
Grounded Search + Source Navigation
 ↓
Review & Export
```
## Supported Documents

The generic upload workflow currently supports **text-based, numbered legal/deposition transcripts** following a continuous 25-line transcript structure.

Scanned, image-only, corrupt, or unsupported layouts may be rejected to preserve reliable source-level provenance.

## Tech Stack

- Python
- FastAPI
- PyMuPDF
- scikit-learn
- SQLite
- HTML / CSS / JavaScript
- Pytest

## Run Locally

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

## Verification

Current automated test result:

**22 tests passed**

The Persis Yu reference workflow and supported uploaded-document workflow maintain separate canonical transcripts, evidence, and indexing runs.

## Submission Commits

**Final submission commit:** `TO_BE_UPDATED`

**Meaningful earlier commit:** `375e1d4`

### What changed and why

Between these commits, DepoIndex was developed from the reference deposition parsing flow into a complete, evidence-grounded legal deposition indexing application.

Key improvements included:
- Improved deposition parsing and canonical transcript handling
- Added topic indexing, topic threads, timeline, and re-entry detection
- Added grounded testimony search and source-line navigation
- Added provenance and integrity validation
- Added supported PDF upload workflow with separate document/run state
- Improved the attorney-facing dashboard and review workflow
- Added JSON/Markdown export support
- Added safeguards so grounded search requires a completed index

These changes were made to provide a reliable, source-grounded workflow for navigating deposition testimony while keeping evidence traceable to the canonical transcript.

## Author

**Saumya Dwivedi**  
B.Tech CSE — Cyber Security & Digital Forensics  
VIT Bhopal Unive