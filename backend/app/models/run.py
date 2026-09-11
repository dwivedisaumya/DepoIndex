from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional

@dataclass
class PipelineRun:
    run_id: str
    timestamp: str
    model: str
    configuration: Dict[str, Any] = field(default_factory=dict)
    number_of_windows: int = 0
    number_of_candidates: int = 0
    number_of_final_topics: int = 0
    number_of_threads: int = 0
    number_of_reentries: int = 0
    coverage_percentage: float = 0.0
    status: str = "completed"
    provenance_errors: int = 0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PipelineRun:
        return cls(**data)
