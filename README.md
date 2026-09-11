# DepoIndex

DepoIndex creates a chronology-first topic index from the supplied Persis Yu deposition. The canonical parsed transcript remains the authority for every page/line citation: topic detection may propose a range, but deterministic validation must approve it before the range is exported.

## Run

Create a Python 3.11+ virtual environment, install the project, then start the API:

```powershell
python -m pip install -e .
python -m uvicorn backend.app.main:app --reload
```

Run `POST /api/runs` to process the complete deposition. The API writes immutable artifacts to `data/runs/<run_id>/`, including `final_index.json` and `topic_index.md`. Use `/docs` for the interactive API. Dashboard, index, timeline/graph data, source navigation, search, integrity, and review endpoints are exposed under `/api`.

## Truthful evaluation status

The included source transcript and parser/provenance tests are present. No completed manual 20-entry review, three-run stability execution, or evaluated failure-case record existed in the supplied project; templates and methodology are documented as **not evaluated** until the commands are run and an attorney records results.
