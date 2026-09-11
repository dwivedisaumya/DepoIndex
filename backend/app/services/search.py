"""Grounded local search. Results always contain canonical source IDs."""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from ..models.topic import TopicSegment, TopicThread
from .provenance import ProvenanceValidator


class GroundedSearch:
    def __init__(self, validator: ProvenanceValidator, segments: Iterable[TopicSegment], threads: Iterable[TopicThread]):
        self.validator, self.segments, self.threads = validator, list(segments), list(threads)

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        terms = {token for token in re.findall(r"[a-z0-9]+", query.lower()) if len(token) > 1}
        if not terms:
            return []
        results = []
        for line in self.validator.lines:
            score = sum(term in line.text.lower() for term in terms)
            if score:
                results.append({"type": "transcript", "score": score, "source_ids": [line.source_id], "citation": f"p. {line.page}:{line.line}", "text": line.text})
        for segment in self.segments:
            haystack = f"{segment.title} {segment.description} {segment.summary or ''}".lower()
            score = sum(term in haystack for term in terms)
            if score:
                results.append({"type": "topic_segment", "score": score, "segment_id": segment.segment_id, "thread_id": segment.thread_id, "source_ids": [segment.start_id, segment.end_id], "citation": f"p. {segment.start_page}:{segment.start_line}–p. {segment.end_page}:{segment.end_line}", "text": segment.summary or segment.description})
        return sorted(results, key=lambda item: (-item["score"], item["citation"]))[:limit]
