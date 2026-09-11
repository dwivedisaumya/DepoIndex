"""Deterministic health checks for a generated topic index."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Set

from ..models.topic import TopicSegment, TopicThread
from .provenance import ProvenanceValidator


@dataclass
class IntegrityReport:
    total_substantive_lines: int
    covered_lines: int
    coverage_percentage: float
    suspicious_gaps: List[Dict[str, Any]]
    invalid_references: List[Dict[str, str]]
    evidence_mismatches: List[Dict[str, str]]
    duplicate_segment_ids: List[str]
    orphan_evidence: List[str]
    uncertain_regions: List[Dict[str, Any]]

    @property
    def healthy(self) -> bool:
        return not (self.invalid_references or self.evidence_mismatches or self.duplicate_segment_ids or self.orphan_evidence)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["healthy"] = self.healthy
        return result


class IndexIntegrityAuditor:
    """Audits source-addressability; it never corrects or invents citations."""

    def __init__(self, validator: ProvenanceValidator, gap_threshold: int = 30):
        self.validator = validator
        self.gap_threshold = gap_threshold

    def audit(self, segments: Iterable[TopicSegment], threads: Iterable[TopicThread] = ()) -> IntegrityReport:
        segments = list(segments)
        covered: Set[str] = set()
        invalid: List[Dict[str, str]] = []
        mismatches: List[Dict[str, str]] = []
        orphan: List[str] = []
        seen: Set[str] = set()
        duplicate: List[str] = []

        for segment in segments:
            if segment.segment_id in seen:
                duplicate.append(segment.segment_id)
            seen.add(segment.segment_id)
            checked = self.validator.validate_reference(segment.start_page, segment.start_line, segment.end_page, segment.end_line)
            if not checked.is_valid:
                invalid.append({"segment_id": segment.segment_id, "error": checked.error_message or "invalid range"})
                continue
            covered.update(checked.source_ids)
            for evidence in segment.evidence:
                evidence_check = self.validator.validate_reference(
                    evidence.start_page, evidence.start_line, evidence.end_page, evidence.end_line, evidence.text
                )
                if not evidence_check.is_valid:
                    mismatches.append({"evidence_id": evidence.evidence_id, "error": evidence_check.error_message or "evidence mismatch"})
                elif not set(evidence.source_ids).issubset(set(evidence_check.source_ids)):
                    orphan.append(evidence.evidence_id)

        substantive = [line for line in self.validator.lines if not line.is_empty and line.text.strip()]
        uncovered = [line for line in substantive if line.source_id not in covered]
        gaps = self._regions(uncovered, self.gap_threshold)
        uncertain = self._regions([line for line in substantive if line.is_colloquy], self.gap_threshold)
        return IntegrityReport(
            total_substantive_lines=len(substantive), covered_lines=len(covered & {line.source_id for line in substantive}),
            coverage_percentage=round(100 * len(covered & {line.source_id for line in substantive}) / len(substantive), 2) if substantive else 0.0,
            suspicious_gaps=gaps, invalid_references=invalid, evidence_mismatches=mismatches,
            duplicate_segment_ids=sorted(set(duplicate)), orphan_evidence=orphan, uncertain_regions=uncertain,
        )

    @staticmethod
    def _regions(lines: List[Any], threshold: int) -> List[Dict[str, Any]]:
        regions: List[Dict[str, Any]] = []
        start = previous = None
        count = 0
        for line in lines:
            coord = (line.page, line.line)
            contiguous = previous is not None and (
                (line.page == previous.page and line.line == previous.line + 1)
                or (line.page == previous.page + 1 and previous.line == 25 and line.line == 1)
            )
            if start is None or not contiguous:
                if start and count >= threshold:
                    regions.append({"start_id": start.source_id, "end_id": previous.source_id, "line_count": count})
                start, count = line, 0
            previous = line
            count += 1
        if start and previous and count >= threshold:
            regions.append({"start_id": start.source_id, "end_id": previous.source_id, "line_count": count})
        return regions
