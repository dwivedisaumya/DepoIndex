# Stability Report

## Status: Not evaluated

No three-run execution evidence was supplied, so no stability result is claimed.

Execute `POST /api/runs` three times against the same canonical transcript and configuration. Compare each generated `final_index.json` for topic count, canonical labels, page/line boundaries, and thread assignments. Preserve the three run IDs and report the actual differences; model-backed runs must additionally record model and temperature.
