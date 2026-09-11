from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

@dataclass
class EvidenceItem:
    evidence_id: str
    start_page: int
    start_line: int
    end_page: int
    end_line: int
    start_id: str
    end_id: str
    source_ids: List[str]
    text: str
    citation: str
    verification_status: str = "verified"
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EvidenceItem:
        return cls(**data)
