# DepoIndex — AI-Powered Deposition Topic Index

DepoIndex is a legal-tech prototype that converts long deposition transcripts into a
**chronological, verifiable Topic Index** while preserving exact source provenance.

The system is designed to help attorneys quickly identify where important subjects
were discussed and independently verify each generated entry against the original
transcript.

> **Prototype Notice:** The application is a functional engineering prototype.
> Production-grade UI or deployment is not expected.

---

## Problem

Long deposition transcripts are difficult to navigate manually.

DepoIndex addresses the problem of:

- identifying meaningful topics and topic transitions
- determining topic start and end boundaries
- preserving page and line references
- handling topics that continue across pages
- handling brief digressions and topic re-entry
- producing a chronologically ordered Topic Index
- allowing an attorney to verify generated entries against the source testimony

The system was developed and validated using the **Persis Yu deposition** supplied
for the technical problem-solving round.

---

## Key Features

- 📄 Persis Yu deposition processing
- 📤 Upload support for compatible text-based legal/deposition PDFs
- 🔎 Grounded testimony search
- 🧵 Topic threads and topic re-entry detection
- 📅 Chronological topic timeline
- 📌 Evidence and source-line navigation
- 🔐 Provenance and integrity checks
- 👩‍⚖️ Human review support
- 📊 JSON and Markdown Topic Index exports

---

## Live Application / Demo

**Live Demo:**  

https://depoindex-1rb4.onrender.com/

The application is deployed as a functional prototype and can be used to
demonstrate the deposition indexing workflow.

---

## How It Works

```text
                    Deposition PDF
                         │
                         ▼
               Transcript Extraction
                         │
                         ▼
             Canonical Transcript
          (page + line provenance)
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
                 Topic Detection
                         │
                         ▼
              Topic Boundary Refinement
                         │
                         ▼
              Evidence / Provenance
                    Validation
                         │
                         ▼
              Topic Threads & Timeline
                         │
                         ▼
             Grounded Search & Review
                         │
                         ▼
                  Export Results
                    /         \
                  JSON       Markdown

``` 
## Architecture Principle

The original transcript remains the source of truth.

Topic detection may use automated/LLM-assisted processing, but page and line coordinates are preserved from the canonical transcript rather than being generated from the topic labels.

## Provenance Strategy

Every Topic Index entry contains enough information to independently locate the supporting testimony in the source transcript.

Each entry preserves:

- Topic
- Start page and line
- End page and line
- Supporting source reference/evidence

The processing pipeline preserves canonical page/line coordinates through:

PDF physical page
↓
Canonical TranscriptLine
↓
Transcript Chunk
↓
Topic Candidate
↓
Boundary Refinement
↓
Evidence Validation
↓
JSON / Markdown Export


A key validation principle is:

> A plausible topic label with an incorrect source location is treated as a failure.

## Topic Segmentation

Deposition transcripts do not contain explicit topic boundaries.

DepoIndex therefore considers the distinction between:

- **New topic** — genuine subject-matter change
- **Continuation** — the current subject continues
- **Brief digression** — a short deviation within a larger topic
- **Re-entry** — a previously discussed subject returns later
- **Related subject** — a closely related but independently useful topic

Topic labels are intended to be grounded in the evidence contained within the associated citation range.

## Supported Documents

The generic upload workflow currently supports text-based, numbered legal or deposition transcripts following a continuous 25-line transcript structure.

Scanned, image-only, corrupt, or unsupported layouts may be rejected in order to preserve reliable source-level provenance.

The Persis Yu deposition is treated as the reference document for the submitted Topic Index and validation work.

## Outputs

The repository includes the generated Topic Index in both required formats:

**JSON**
`output/depoindex-index (1).json`

**Human-readable Markdown**
`output/depoindex-topic-index (1).md`

Each Topic Index entry contains:

- Topic
- Start page/line
- End page/line
- Supporting source reference/evidence

## Validation

The system was manually evaluated using at least 20 Topic Index entries from the Persis Yu deposition.

The validation evaluated:

- Location accuracy
- Topic relevance
- Boundary quality
- Coverage
- Redundancy

The evaluation methodology and detailed results are documented in:

- `docs/validation_report.md`
- `docs/DepoIndex_Complete_Validation_Report.pdf`

## Stability Testing

A three-run stability analysis was performed over the reviewed deposition range.

The validation documentation records:

- topic-count variation
- topic-title consistency
- citation/location consistency
- boundary consistency
- topics appearing/disappearing between segmentations
- limitations of the repeated-run methodology

The stability analysis is documented in:

- `docs/stability_report.md`

Because the underlying automated pipeline was not available for repeated execution in the validation environment, the additional runs are explicitly documented as **manual proxy runs**, rather than being represented as genuine automated reruns.

## Failure Analysis

The validation identified three major failure categories:

- Citation/page-location issues identified during manual comparison
- Topic-label mismatch with cited evidence
- Over-segmentation, overlapping ranges, and nested citation ranges

Each failure case documents:

- what the system produced
- what should have been produced
- why the failure occurred
- proposed corrective action

Detailed analysis:

- `docs/failure_analysis.md`

## Validation Documents

The repository contains the complete validation documentation:

docs/
├── validation_report.md
├── stability_report.md
├── failure_analysis.md
└── DepoIndex_Complete_Validation_Report.pdf


Additional project documentation includes:

docs/
├── architecture.md
├── methodology.md
├── document_analysis.md
├── compliance_audit.md
└── llm_usage.md


## Tech Stack

- Python
- FastAPI
- PyMuPDF
- scikit-learn
- SQLite
- HTML / CSS / JavaScript
- Pytest

## Run Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install the project and development dependencies:

```bash
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Run the test suite:

```bash
.\.venv\Scripts\python.exe -m pytest -q
```

Start the application:

```bash
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

Then open:

http://127.0.0.1:8000/


## Testing

The current automated test suite reports:

**22 tests passed**

The project maintains separate canonical transcript, evidence, and indexing state for the Persis Yu reference workflow and supported uploaded-document workflow.

## AI / LLM Usage

AI coding and reasoning tools were used during development and validation.

The repository documents significant AI/LLM use, including:

- development assistance
- debugging and investigation
- architecture and implementation suggestions
- validation/reporting assistance
- review of generated work

Important AI-generated work was reviewed against the source transcript, repository implementation, test results, and validation requirements.

Detailed documentation:

- `docs/llm_usage.md`



## Assignment Deliverables

This repository contains the required Problem #3 deliverables:

**GitHub Repository**
- Working source code
- README with setup and execution instructions
- Dependencies/environment configuration
- `llm_usage.md`
- Meaningful Git development history

**Working Application**
- A deployed functional prototype is provided through the Live Demo URL above.

**Topic Index**
- JSON output
- Human-readable Markdown output

**Validation Report**
- Evaluation methodology
- Results from at least 20 reviewed entries
- Three-run stability analysis
- Three failure cases
- Limitations

**Presentation**
- 3–5 slide presentation
  - Architecture
  - Topic segmentation
  - Provenance strategy
  - Example Topic Index
  - Validation results
  - Stability/failure analysis
  - Limitations and next steps

## Git Development History

The repository was developed incrementally rather than as a single final commit.

**Final Submission Commit**

`7ecae12`

**Meaningful Earlier Commit**

`375e1d4`

## What Changed and Why

The project evolved from the initial deposition parsing workflow into a more complete deposition indexing application.

Major improvements included:

- improved deposition parsing and canonical transcript handling
- topic indexing and topic-thread support
- chronology/timeline functionality
- grounded testimony search
- source-level navigation
- provenance and integrity validation
- supported PDF upload workflow
- human review support
- JSON and Markdown exports
- safeguards around grounded search and completed indexing

These changes were made to improve traceability, reviewability, and attorney usability while keeping the canonical transcript as the source of truth.

## Limitations

DepoIndex is a prototype and should not be treated as an autonomous legal decision-making system.

Current limitations include:

- Topic granularity can vary for long discursive testimony.
- Topic boundaries require stronger deterministic controls.
- Automated provenance verification should be strengthened further.
- The current generic upload workflow supports a constrained transcript format.
- Stability should be measured using repeated executions of the actual automated pipeline under controlled deterministic settings.
- Human review remains important before relying on generated topic boundaries or labels.

The validation reports document these limitations and proposed improvements in greater detail.

## Future Improvements

Planned improvements include:

- deterministic repeated-run stability testing
- stronger automated citation verification
- improved topic merge/de-duplication
- explicit overlap and nested-range detection
- fixed segmentation/granularity rules
- stronger evidence-grounded topic labeling
- controlled topic taxonomy
- scaling the workflow to larger deposition collections

## Author

**Saumya Dwivedi**
B.Tech CSE — Cyber Security & Digital Forensics
VIT Bhopal University







