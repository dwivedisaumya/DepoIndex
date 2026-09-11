from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class TranscriptLine:
    source_id: str
    page: int
    line: int
    text: str
    raw_text: str
    speaker: Optional[str] = None
    timestamp: Optional[str] = None
    is_question: bool = False
    is_answer: bool = False
    is_colloquy: bool = False
    is_empty: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TranscriptLine:
        return cls(**data)

@dataclass
class TranscriptWindow:
    window_id: str
    start_id: str
    end_id: str
    start_page: int
    start_line: int
    end_page: int
    end_line: int
    source_ids: List[str]
    lines: List[TranscriptLine]
    text: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["lines"] = [line.to_dict() if isinstance(line, TranscriptLine) else line for line in self.lines]
        return d
