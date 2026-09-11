"""Grounded local search. Results always contain canonical source IDs."""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        # TF-IDF adds conceptual ranking beyond exact term-count ordering while
        # retaining the exact canonical citations returned above.
        if results:
            corpus = [item["text"] for item in results]
            matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus + [query])
            semantic_scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
            for item, semantic_score in zip(results, semantic_scores):
                item["semantic_score"] = round(float(semantic_score), 4)
        return sorted(results, key=lambda item: (-item.get("semantic_score", 0), -item["score"], item["citation"]))[:limit]
