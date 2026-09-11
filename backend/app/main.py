"""FastAPI application for the attorney-facing DepoIndex workspace."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .services.pipeline import DepoIndexPipeline
from .services.provenance import ProvenanceValidator
from .services.search import GroundedSearch

app = FastAPI(title="DepoIndex", version="0.1.0")
LATEST: Dict[str, Any] = {}

class ReviewRequest(BaseModel):
    status: str
    revised_title: str | None = None
    notes: str | None = None

def current() -> Dict[str, Any]:
    if not LATEST:
        raise HTTPException(404, "No pipeline run is loaded. POST /api/runs first.")
    return LATEST

@app.post("/api/runs")
def run_pipeline() -> Dict[str, Any]:
    global LATEST
    LATEST = DepoIndexPipeline().run()
    return LATEST

@app.get("/", include_in_schema=False)
def workspace() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")

@app.get("/api/dashboard")
def dashboard() -> Dict[str, Any]:
    data = current(); return {"run": data["run"], "integrity": data["integrity"]}

@app.get("/api/topics")
def topics() -> list[Dict[str, Any]]:
    return current()["segments"]

@app.get("/api/threads")
def threads() -> list[Dict[str, Any]]:
    return current()["threads"]

@app.get("/api/relationships")
def relationships() -> list[Dict[str, Any]]:
    return current()["relationships"]

@app.get("/api/integrity")
def integrity() -> Dict[str, Any]:
    return current()["integrity"]

@app.get("/api/source/{page}/{line}")
def source(page: int, line: int) -> Dict[str, Any]:
    item = ProvenanceValidator.from_canonical_file()._coord_map.get((page, line))
    if not item: raise HTTPException(404, "Transcript line does not exist")
    return item.to_dict()

@app.get("/api/source/{page}/{line}/topics")
def source_topics(page: int, line: int) -> list[Dict[str, Any]]:
    """Bidirectional source-to-topic navigation, based solely on verified ranges."""
    current()
    return [segment for segment in LATEST["segments"] if (segment["start_page"], segment["start_line"]) <= (page, line) <= (segment["end_page"], segment["end_line"])]

@app.get("/api/search")
def search(q: str) -> list[Dict[str, Any]]:
    data = current()
    validator = ProvenanceValidator.from_canonical_file()
    # API payloads stay JSON-native; construct only the fields search needs.
    from .models.topic import TopicSegment, TopicThread, TopicConfidence
    from .models.evidence import EvidenceItem
    fields = set(TopicSegment.__dataclass_fields__)
    segments = [TopicSegment(**{key: value for key, value in s.items() if key in fields and key not in {"evidence", "confidence"}}, evidence=[EvidenceItem(**e) for e in s["evidence"]], confidence=TopicConfidence(**s["confidence"])) for s in data["segments"]]
    threads = [TopicThread(thread_id=t["thread_id"], canonical_title=t["canonical_title"], description=t["description"], category=t["category"]) for t in data["threads"]]
    return GroundedSearch(validator, segments, threads).search(q)

@app.post("/api/topics/{segment_id}/review")
def review(segment_id: str, review: ReviewRequest) -> Dict[str, Any]:
    data = current()
    item = next((s for s in data["segments"] if s["segment_id"] == segment_id), None)
    if not item: raise HTTPException(404, "Topic segment does not exist")
    item.setdefault("attorney_review", {})
    item["attorney_review"] = review.model_dump()
    return item
