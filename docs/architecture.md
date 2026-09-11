# System Architecture: DepoIndex

## 1. Architectural Philosophy

> **AI proposes. Deterministic systems verify. Attorney reviews.**

Traditional legal AI systems suffer from hallucinated citations, lost page references, and boundary drift. DepoIndex departs radically from the "Upload PDF → Ask AI → Get Summary" paradigm. It implements a **provenance-first, verification-enforced intelligence workspace**:

```
[Raw Deposition PDF]
        │
        ▼
[Deterministic Provenance Parser] ────► [Canonical Transcript (Source of Truth)]
        │                                         ▲
        ▼                                         │
[Provenance-Preserving Windows]                   │
        │                                         │
        ▼                                         │
[Candidate Topic Proposal (LLM / Heuristic)]      │ (Every reference strictly verified)
        │                                         │
        ▼                                         │
[Deterministic Boundary Refinement & Validation] ─┘
        │
        ▼
[Topic Thread & Re-Entry Engine]
        │
        ▼
[Topic Relationship Graph & Index Integrity Engine]
        │
        ▼
[FastAPI REST API + SQLite Layer]
        │
        ▼
[React 18 + TypeScript + Tailwind Attorney Workspace]
```

---

## 2. Differentiators & Core Abstractions

### A. Topic Threads vs. Topic Segments
A flat list of topics fails when an attorney needs to know if a witness touched on a subject, moved on to an exhibit, and returned to the subject 40 pages later.
- **`Topic Thread` (Semantic Subject):** A global subject discussed during the deposition (e.g., `Employment History`, `Access Group Servicing Disclosures`, `Navient Transition`).
- **`Topic Segment` (Physical Occurrence):** A specific chronological occurrence bounded by exact `start_page:line` and `end_page:line` coordinates (e.g., Segment 1: Page 10 Line 23 → Page 16 Line 8; Segment 2: Page 83 Line 2 → Page 86 Line 11).
- **`RE_ENTERS` Relationship:** When a subsequent segment reactivates an earlier Topic Thread after intervening topics, the system links them via a directional `re-enters` relationship edge.

### B. The 4-Tier Evidence Chain
Traceability is mathematically enforced:
```
[TOPIC THREAD] (e.g., TT03: Student Loan Policy & Advocacy)
      │
      ▼
[TOPIC SEGMENT] (e.g., S03A: Page 12 Line 4 → Page 16 Line 8)
      │
      ▼
[VERIFIED EVIDENCE SPAN] (e.g., Page 12 Lines 8–18, exact text excerpt)
      │
      ▼
[CANONICAL TRANSCRIPT LINE] (e.g., p12_l08, p12_l09, ... p12_l18)
```
If an evidence span does not exist in the canonical transcript, or the text differs by even a single character from the source, the reference is rejected with `PROVENANCE_ERROR`.

### C. Index Integrity Diagnostic System
Answers the critical engineering challenge: *"How do you detect if part of the transcript was silently skipped?"*
- Calculates coverage across all 2,032 substantive transcript lines.
- Identifies **Indexed Regions**, **Uncertain Regions**, and **Suspicious Gaps** (unindexed stretches exceeding configurable thresholds).
- Audits for duplicate topic IDs, orphan evidence nodes, and broken sequence transitions.

---

## 3. Modular Backend Architecture (`backend/app/`)

### A. Data Models (`models/`)
- `TranscriptLine`: Canonical representation (`source_id`, `page`, `line`, `text`, `speaker`, `timestamp`, `raw_text`).
- `TopicThread`: Semantic topic entity (`id`, `title`, `description`, `canonical_label`, `category`).
- `TopicSegment`: Physical chronological occurrence (`id`, `thread_id`, `start_page`, `start_line`, `end_page`, `end_line`, `confidence`).
- `EvidenceItem`: Verifiable excerpt (`id`, `segment_id`, `start_page`, `start_line`, `end_page`, `end_line`, `text`, `source_ids`, `verification_status`).
- `TopicRelationship`: Graph edges (`id`, `source_id`, `target_id`, `relation_type`: `continues`, `re-enters`, `related-to`, `digresses-to`, `overlaps-with`).
- `AttorneyReview`: Non-destructive review overlay (`id`, `topic_id`, `status`: `ACCEPTED`/`EDITED`/`REJECTED`/`NEEDS_REVIEW`, `revised_start`, `revised_end`, `revised_title`, `notes`, `updated_at`).
- `PipelineRun`: Run ledger for reproducibility (`run_id`, `timestamp`, `model`, `config`, `metrics`).

### B. Core Services (`services/`)
1. **`parser.py`:** Extracts 100% of line blocks from PDF, identifies empty slots, parses speakers/timestamps, and writes immutable `processed_transcript.json`.
2. **`provenance.py`:** Deterministic validator with `validate_reference()` and `get_source_text()`. Returns exact text slices or raises `PROVENANCE_ERROR`.
3. **`chunker.py`:** Generates structured, overlapping transcript windows (`processed_windows.json`) retaining full line IDs.
4. **`topic_detector.py`:** Proposes candidate topics with evidence IDs. Supports OpenAI/Gemini structured outputs with deterministic semantic fallback.
5. **`boundary_refiner.py`:** Resolves candidate boundaries to real Q&A pairs; detects digressions and cross-page continuations.
6. **`reentry_detector.py`:** Compares semantic embeddings and topic labels across the deposition timeline to identify re-entries.
7. **`graph_builder.py`:** Constructs the interactive topic relationship graph (threads, segments, evidence, relations).
8. **`search.py`:** Grounded semantic search over topic threads, segments, and testimony lines with exact provenance citations.
9. **`integrity.py`:** Audits coverage gaps, line continuity, and verification health.
10. **`exporter.py`:** Generates JSON, Markdown, and self-contained HTML exports.

---

## 4. Frontend Architecture (`frontend/src/`)

Built with React 18, TypeScript, Tailwind CSS, and Lucide icons:
- **`Dashboard`:** Executive KPI metrics (Total Topics, Verified Topics, Topic Threads, Re-entries, Line Coverage %, Provenance Errors = 0).
- **`TopicIndex`:** Chronological master index with sorting, confidence badges, verification pills, and expandable evidence chains.
- **`Timeline`:** Vertical interactive deposition timeline illustrating chronological topic progression and re-entry points.
- **`TopicThreads`:** Dedicated thread view showing multi-segment evolution and re-entries across pages.
- **`TopicGraph`:** Interactive SVG/Canvas node-link visualization of topic relationships (`continues`, `re-enters`, `related-to`).
- **`SourceViewer`:** Dual-pane bidirectional transcript reader with line numbering, speaker tags, and instant jump-to-citation highlighting.
- **`SemanticSearch`:** Fast keyword and conceptual search yielding verified testimony excerpts.
- **`ValidationView`:** Detailed review table of 20+ evaluated entries with accuracy, boundary, and redundancy scores.
- **`IndexIntegrity`:** Real-time health diagnostic dashboard with gap detection and verification checkmarks.
- **`AttorneyReviewModal`:** Human-in-the-loop review interface preserving separate AI proposal vs. Attorney revised states.

---

## 5. Persistence & Reproducibility Strategy

1. **SQLite Database (`data/depoindex.db`):** Lightweight, relational persistence storing all lines, threads, segments, relationships, reviews, and runs.
2. **Run Artifact Storage (`data/runs/<run_id>/`):** Every pipeline execution writes immutable snapshots:
   - `parsed_transcript.json`
   - `windows.json`
   - `candidate_topics.json`
   - `refined_topics.json`
   - `final_index.json`
   - `run_metadata.json`
3. **Deterministic Testing:** Automated test suites in `tests/` verify parser correctness, provenance validation edge cases, boundary rules, and stability metrics.
