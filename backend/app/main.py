"""FastAPI application for the attorney-facing DepoIndex workspace."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .services.pipeline import DepoIndexPipeline
from .services.provenance import ProvenanceValidator
from .services.search import GroundedSearch
from .services.review_store import ReviewStore

app = FastAPI(title="DepoIndex", version="0.1.0")
LATEST: Dict[str, Any] = {}

class ReviewRequest(BaseModel):
    status: Literal["ACCEPTED", "EDITED", "REJECTED", "FLAGGED_FOR_REVIEW"]
    revised_title: str | None = None
    revised_description: str | None = None
    revised_start_page: int | None = None
    revised_start_line: int | None = None
    revised_end_page: int | None = None
    revised_end_line: int | None = None
    notes: str | None = None
    reviewed_by: str = "Attorney Reviewer"

def current() -> Dict[str, Any]:
    if not LATEST:
        raise HTTPException(404, "No pipeline run is loaded. POST /api/runs first.")
    return LATEST

@app.post("/api/runs")
def run_pipeline() -> Dict[str, Any]:
    global LATEST
    LATEST = DepoIndexPipeline().run()
    return LATEST

@app.post("/api/parse")
def parse_deposition() -> Dict[str, Any]:
    """Parse the supplied deposition into the canonical source-of-truth artifact."""
    return DepoIndexPipeline().parse_source()

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

@app.get("/api/source-range")
def source_range(start_page: int, start_line: int, end_page: int, end_line: int) -> list[Dict[str, Any]]:
    """Return an independently verified, highlightable canonical transcript span."""
    validator = ProvenanceValidator.from_canonical_file()
    checked = validator.validate_reference(start_page, start_line, end_page, end_line)
    if not checked.is_valid:
        raise HTTPException(422, checked.error_message or "Invalid source range")
    return [validator._id_map[source_id].to_dict() for source_id in checked.source_ids]

@app.get("/api/source/{page}/{line}/topics")
def source_topics(page: int, line: int) -> list[Dict[str, Any]]:
    """Bidirectional source-to-topic navigation, based solely on verified ranges."""
    current()
    if (page, line) not in ProvenanceValidator.from_canonical_file()._coord_map:
        raise HTTPException(404, "Transcript line does not exist")
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
    revision = review.model_dump(exclude={"status", "reviewed_by"}, exclude_none=True)
    return ReviewStore().save(segment_id, data["run"]["run_id"], review.status, item.copy(), revision, review.reviewed_by)

@app.get("/api/topics/{segment_id}/reviews")
def reviews(segment_id: str) -> list[Dict[str, Any]]:
    current()
    return ReviewStore().list_for_segment(segment_id)
