from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class AttorneyReview:
    review_id: str
    topic_id: str
    status: str  # ACCEPTED, EDITED, REJECTED, FLAGGED_FOR_REVIEW
    original_title: str
    original_start_page: int
    original_start_line: int
    original_end_page: int
    original_end_line: int
    revised_title: Optional[str] = None
    revised_description: Optional[str] = None
    revised_start_page: Optional[int] = None
    revised_start_line: Optional[int] = None
    revised_end_page: Optional[int] = None
    revised_end_line: Optional[int] = None
    notes: Optional[str] = None
    reviewed_by: str = "Attorney Reviewer"
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AttorneyReview:
        return cls(**data)
