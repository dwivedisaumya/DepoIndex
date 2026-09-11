from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional
from .evidence import EvidenceItem

@dataclass
class TopicConfidence:
    topic_relevance: str = "high"
    boundary: str = "high"
    provenance: str = "verified"

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

@dataclass
class TopicSegment:
    segment_id: str
    thread_id: str
    topic_id: str
    title: str
    description: str
    start_page: int
    start_line: int
    end_page: int
    end_line: int
    start_id: str
    end_id: str
    evidence: List[EvidenceItem] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)
    relationship_type: str = "primary"
    is_reentry: bool = False
    confidence: TopicConfidence = field(default_factory=TopicConfidence)
    verification_status: str = "verified"
    summary: Optional[str] = None
    attorney_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["confidence"] = self.confidence.to_dict() if isinstance(self.confidence, TopicConfidence) else self.confidence
        d["evidence"] = [e.to_dict() if isinstance(e, EvidenceItem) else e for e in self.evidence]
        return d

@dataclass
class TopicThread:
    thread_id: str
    canonical_title: str
    description: str
    category: str
    segments: List[TopicSegment] = field(default_factory=list)
    related_thread_ids: List[str] = field(default_factory=list)
    has_reentry: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["segments"] = [s.to_dict() if isinstance(s, TopicSegment) else s for s in self.segments]
        return d

@dataclass
class TopicRelationship:
    id: str
    source_id: str
    target_id: str
    relationship_type: str  # continues, re-enters, related-to, overlaps-with, digresses-to
    source_type: str = "segment" # thread or segment
    target_type: str = "segment"
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
