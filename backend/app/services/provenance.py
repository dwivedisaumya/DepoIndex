from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
from pathlib import Path

from ..models.transcript import TranscriptLine
from .parser import DepositionParser

@dataclass
class ProvenanceValidationResult:
    is_valid: bool
    status: str  # "VERIFIED" or "PROVENANCE_ERROR"
    error_message: Optional[str] = None
    start_id: Optional[str] = None
    end_id: Optional[str] = None
    source_ids: List[str] = None
    canonical_text: Optional[str] = None
    matched_excerpt: bool = True

    def __post_init__(self):
        if self.source_ids is None:
            self.source_ids = []

class ProvenanceValidator:
    """
    Deterministic provenance validation engine.
    Guarantees every cited reference strictly corresponds to canonical source testimony.
    """

    def __init__(self, canonical_lines: List[TranscriptLine]):
        self.lines = canonical_lines
        self.min_page = min(l.page for l in canonical_lines) if canonical_lines else 7
        self.max_page = max(l.page for l in canonical_lines) if canonical_lines else 88
        self._coord_map: Dict[Tuple[int, int], TranscriptLine] = {
            (l.page, l.line): l for l in canonical_lines
        }
        self._id_map: Dict[str, TranscriptLine] = {
            l.source_id: l for l in canonical_lines
        }

    @classmethod
    def from_canonical_file(cls, json_path: str | Path = "data/processed/processed_transcript.json") -> ProvenanceValidator:
        parser = DepositionParser("data/raw/Persis_Yu_Deposition_Problem_statement.pdf")
        lines = parser.load_canonical(json_path)
        return cls(lines)

    def get_source_text(self, start_page: int, start_line: int, end_page: int, end_line: int) -> str:
        """
        Retrieve exact concatenated source text for the specified coordinate range.
        Raises ValueError if coordinates are invalid.
        """
        val = self.validate_reference(start_page, start_line, end_page, end_line)
        if not val.is_valid:
            raise ValueError(f"Invalid reference range: {val.error_message}")
        return val.canonical_text or ""

    def validate_reference(
        self,
        start_page: int,
        start_line: int,
        end_page: int,
        end_line: int,
        excerpt: Optional[str] = None
    ) -> ProvenanceValidationResult:
        """
        Verify that:
        1. Pages exist in the canonical deposition.
        2. Lines exist (1..25).
        3. Range is valid (start <= end).
        4. Non-empty testimony exists within the range.
        5. Excerpt strictly matches canonical source text if supplied.
        """
        start_id = f"p{start_page:02d}_l{start_line:02d}"
        end_id = f"p{end_page:02d}_l{end_line:02d}"

        # 1. Page boundary checks
        if start_page < self.min_page or start_page > self.max_page:
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"Start page {start_page} out of bounds ({self.min_page}..{self.max_page})",
                start_id=start_id,
                end_id=end_id
            )

        if end_page < self.min_page or end_page > self.max_page:
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"End page {end_page} out of bounds ({self.min_page}..{self.max_page})",
                start_id=start_id,
                end_id=end_id
            )

        # 2. Line boundary checks
        if not (1 <= start_line <= 25):
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"Start line {start_line} out of bounds (1..25)",
                start_id=start_id,
                end_id=end_id
            )

        if not (1 <= end_line <= 25):
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"End line {end_line} out of bounds (1..25)",
                start_id=start_id,
                end_id=end_id
            )

        # 3. Coordinate ordering check
        if (start_page, start_line) > (end_page, end_line):
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"Reversed range: ({start_page}:{start_line}) > ({end_page}:{end_line})",
                start_id=start_id,
                end_id=end_id
            )

        # 4. Collect line objects
        range_lines: List[TranscriptLine] = []
        source_ids: List[str] = []

        curr_p, curr_l = start_page, start_line
        while (curr_p, curr_l) <= (end_page, end_line):
            line_obj = self._coord_map.get((curr_p, curr_l))
            if line_obj:
                range_lines.append(line_obj)
                source_ids.append(line_obj.source_id)

            curr_l += 1
            if curr_l > 25:
                curr_l = 1
                curr_p += 1

        if not range_lines:
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"No lines found in range ({start_page}:{start_line} to {end_page}:{end_line})",
                start_id=start_id,
                end_id=end_id
            )

        # Ensure range contains at least some non-empty testimony
        non_empty_texts = [l.text for l in range_lines if not l.is_empty and l.text.strip()]
        if not non_empty_texts:
            return ProvenanceValidationResult(
                is_valid=False,
                status="PROVENANCE_ERROR",
                error_message=f"Range contains only blank/unpopulated lines ({start_id}..{end_id})",
                start_id=start_id,
                end_id=end_id,
                source_ids=source_ids
            )

        canonical_text = " ".join(non_empty_texts)

        # 5. Excerpt validation
        if excerpt is not None:
            cleaned_excerpt = " ".join(excerpt.split())
            cleaned_canonical = " ".join(canonical_text.split())

            # Check substring inclusion
            if cleaned_excerpt.lower() not in cleaned_canonical.lower():
                # Allow partial prefix match if excerpt was truncated with ellipsis
                truncated = cleaned_excerpt.rstrip(".").rstrip()
                if len(truncated) < 15 or truncated.lower() not in cleaned_canonical.lower():
                    return ProvenanceValidationResult(
                        is_valid=False,
                        status="PROVENANCE_ERROR",
                        error_message="Evidence excerpt does not match canonical transcript text",
                        start_id=start_id,
                        end_id=end_id,
                        source_ids=source_ids,
                        canonical_text=canonical_text,
                        matched_excerpt=False
                    )

        return ProvenanceValidationResult(
            is_valid=True,
            status="VERIFIED",
            error_message=None,
            start_id=start_id,
            end_id=end_id,
            source_ids=source_ids,
            canonical_text=canonical_text,
            matched_excerpt=True
        )
