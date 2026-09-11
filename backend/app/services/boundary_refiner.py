from __future__ import annotations
from typing import List, Dict, Tuple, Optional
from pathlib import Path

from ..models.transcript import TranscriptLine
from ..models.topic import TopicSegment, TopicConfidence
from ..models.evidence import EvidenceItem
from .provenance import ProvenanceValidator
from .topic_detector import CandidateTopic

class TopicBoundaryRefiner:
    """
    Refines candidate topic boundaries into deterministic, verified Topic Segments.
    Snaps boundaries to full Q&A pairs, merges adjacent window continuations,
    and isolates brief procedural digressions.
    """

    def __init__(self, validator: ProvenanceValidator):
        self.validator = validator
        self._coord_map = validator._coord_map

    def refine_candidates(self, candidates: List[CandidateTopic]) -> List[TopicSegment]:
        if not candidates:
            return []

        # Sort candidates chronologically
        sorted_candidates = sorted(
            candidates,
            key=lambda c: (c.candidate_start_page, c.candidate_start_line)
        )

        # 1. Merge adjacent continuations with the same label
        merged_ranges: List[CandidateTopic] = []
        for cand in sorted_candidates:
            if not merged_ranges:
                merged_ranges.append(cand)
                continue

            last = merged_ranges[-1]
            # Check if labels match and ranges touch or overlap
            is_same_label = (last.label.strip().lower() == cand.label.strip().lower())
            is_contiguous = (
                (cand.candidate_start_page < last.candidate_end_page) or
                (cand.candidate_start_page == last.candidate_end_page and
                 cand.candidate_start_line <= last.candidate_end_line + 5)
            )

            if is_same_label and is_contiguous:
                # Extend end boundary
                if (cand.candidate_end_page, cand.candidate_end_line) > (last.candidate_end_page, last.candidate_end_line):
                    last.candidate_end_page = cand.candidate_end_page
                    last.candidate_end_line = cand.candidate_end_line
                last.evidence_source_ids = list(dict.fromkeys(last.evidence_source_ids + cand.evidence_source_ids))
            else:
                merged_ranges.append(cand)

        # 2. Refine boundaries against Q&A alignment and validate
        segments: List[TopicSegment] = []
        for idx, item in enumerate(merged_ranges):
            sp, sl = self._snap_to_question_start(item.candidate_start_page, item.candidate_start_line)
            ep, el = self._snap_to_answer_end(item.candidate_end_page, item.candidate_end_line)

            # Validate refined coordinates
            val = self.validator.validate_reference(sp, sl, ep, el)
            if not val.is_valid:
                # Fallback to original candidate coordinates if snapping erred
                val = self.validator.validate_reference(
                    item.candidate_start_page, item.candidate_start_line,
                    item.candidate_end_page, item.candidate_end_line
                )
                if val.is_valid:
                    sp, sl = item.candidate_start_page, item.candidate_start_line
                    ep, el = item.candidate_end_page, item.candidate_end_line

            if not val.is_valid:
                continue

            # Build verified evidence items
            evidence_items = self._build_evidence_items(sp, sl, ep, el, item.evidence_source_ids)

            seg_id = f"S{idx + 1:02d}A"
            topic_id = f"T{idx + 1:02d}"

            segment = TopicSegment(
                segment_id=seg_id,
                thread_id="", # Assigned by ReentryDetector in next phase
                topic_id=topic_id,
                title=item.label,
                description=item.description,
                start_page=sp,
                start_line=sl,
                end_page=ep,
                end_line=el,
                start_id=f"p{sp:02d}_l{sl:02d}",
                end_id=f"p{ep:02d}_l{el:02d}",
                evidence=evidence_items,
                confidence=TopicConfidence(
                    topic_relevance="high",
                    boundary="high" if (sp, sl) != (item.candidate_start_page, item.candidate_start_line) else "medium",
                    provenance="verified"
                ),
                verification_status="verified",
                summary=item.description
            )
            segments.append(segment)

        return segments

    def _snap_to_question_start(self, page: int, line: int) -> Tuple[int, int]:
        """Scan backwards up to 3 lines to find the nearest initiating question or colloquy."""
        cur_p, cur_l = page, line
        for _ in range(4):
            line_obj = self._coord_map.get((cur_p, cur_l))
            if line_obj:
                if line_obj.is_question or (line_obj.speaker and "PURCELL" in line_obj.speaker):
                    return cur_p, cur_l
            cur_l -= 1
            if cur_l < 1:
                cur_l = 25
                cur_p -= 1
                if cur_p < self.validator.min_page:
                    break
        return page, line

    def _snap_to_answer_end(self, page: int, line: int) -> Tuple[int, int]:
        """Scan forwards up to 3 lines to include the completion of the witness's answer."""
        cur_p, cur_l = page, line
        for _ in range(4):
            line_obj = self._coord_map.get((cur_p, cur_l))
            if line_obj and line_obj.is_question and (cur_p, cur_l) > (page, line):
                # Stop right before next question starts
                return self._prev_coord(cur_p, cur_l)
            cur_l += 1
            if cur_l > 25:
                cur_l = 1
                cur_p += 1
                if cur_p > self.validator.max_page:
                    break
        return page, line

    def _prev_coord(self, page: int, line: int) -> Tuple[int, int]:
        if line > 1:
            return page, line - 1
        return max(self.validator.min_page, page - 1), 25

    def _build_evidence_items(
        self,
        start_page: int,
        start_line: int,
        end_page: int,
        end_line: int,
        preferred_ids: List[str]
    ) -> List[EvidenceItem]:
        """Build validated EvidenceItem objects within the segment boundaries."""
        ev_items: List[EvidenceItem] = []

        # Find key substantive excerpt (first 3-5 lines of segment)
        excerpt_lines = []
        curr_p, curr_l = start_page, start_line
        count = 0
        while (curr_p, curr_l) <= (end_page, end_line) and count < 6:
            line_obj = self._coord_map.get((curr_p, curr_l))
            if line_obj and not line_obj.is_empty:
                excerpt_lines.append(line_obj)
                count += 1
            curr_l += 1
            if curr_l > 25:
                curr_l = 1
                curr_p += 1

        if excerpt_lines:
            ev_start = excerpt_lines[0]
            ev_end = excerpt_lines[-1]
            excerpt_text = " ".join(l.text for l in excerpt_lines)
            citation = f"p. {ev_start.page}:{ev_start.line}–{ev_end.line}" if ev_start.page == ev_end.page else f"p. {ev_start.page}:{ev_start.line}–p. {ev_end.page}:{ev_end.line}"

            ev_item = EvidenceItem(
                evidence_id=f"ev_{ev_start.source_id}",
                start_page=ev_start.page,
                start_line=ev_start.line,
                end_page=ev_end.page,
                end_line=ev_end.line,
                start_id=ev_start.source_id,
                end_id=ev_end.source_id,
                source_ids=[l.source_id for l in excerpt_lines],
                text=excerpt_text,
                citation=citation,
                verification_status="verified"
            )
            ev_items.append(ev_item)

        return ev_items
