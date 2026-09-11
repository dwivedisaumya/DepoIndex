# DepoIndex

DepoIndex creates a chronology-first topic index from the supplied Persis Yu deposition. The canonical parsed transcript remains the authority for every page/line citation: topic detection may propose a range, but deterministic validation must approve it before the range is exported.

## Run

Create a Python 3.11+ virtual environment, install the project, then start the API:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest -q
python -m backend.app.cli parse
python -m backend.app.cli run
python -m uvicorn backend.app.main:app --reload
```

Run `POST /api/runs` to process the complete deposition. The API writes immutable artifacts to `data/runs/<run_id>/`, including `final_index.json` and `topic_index.md`. Use `/docs` for the interactive API. Dashboard, index, timeline/graph data, source navigation, search, integrity, and review endpoints are exposed under `/api`. Attorney reviews are stored separately in `data/depoindex.db`; they never overwrite an AI proposal.

The browser demo’s first button reparses the supplied PDF; the second creates a complete, exportable index run. See `docs/compliance_audit.md` for requirement-level status.

## Supported input

Persis Yu remains the default Problem #3 reference case and uses its established transcript-page range (7–88). Uploads are accepted only for text-based PDFs with a continuous, numbered 25-line legal-transcript layout. Scanned/image-only, corrupt, empty, mixed-layout, or otherwise unsupported PDFs are rejected with an error; DepoIndex does not use the Persis Yu document as a fallback for an upload.

## Truthful evaluation status

The included source transcript and parser/provenance tests are present. No completed manual 20-entry review, three-run stability execution, or evaluated failure-case record existed in the supplied project; templates and methodology are documented as **not evaluated** until the commands are run and an attorney records results.
