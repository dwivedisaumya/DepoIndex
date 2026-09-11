from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models.transcript import TranscriptLine, TranscriptWindow
from .parser import DepositionParser

class TranscriptChunker:
    """
    Creates provenance-preserving structured transcript windows.
    Guarantees page/line mapping is completely preserved across window boundaries.
    """

    def __init__(self, lines: List[TranscriptLine], window_size: int = 50, overlap: int = 10):
        # We chunk across non-empty substantive lines
        self.all_lines = lines
        self.substantive_lines = [l for l in lines if not l.is_empty]
        self.window_size = window_size
        self.overlap = overlap
        self.windows: List[TranscriptWindow] = []

    @classmethod
    def from_canonical_file(
        cls,
        json_path: str | Path = "data/processed/processed_transcript.json",
        window_size: int = 50,
        overlap: int = 10
    ) -> TranscriptChunker:
        parser = DepositionParser("data/raw/Persis_Yu_Deposition_Problem_statement.pdf")
        lines = parser.load_canonical(json_path)
        return cls(lines, window_size=window_size, overlap=overlap)

    def create_windows(self) -> List[TranscriptWindow]:
        """Generate sliding structured windows with strict coordinate preservation."""
        self.windows = []
        step = max(1, self.window_size - self.overlap)
        total_substantive = len(self.substantive_lines)

        window_idx = 1
        for start_idx in range(0, total_substantive, step):
            end_idx = min(start_idx + self.window_size, total_substantive)
            chunk_lines = self.substantive_lines[start_idx:end_idx]

            if not chunk_lines:
                break

            first_line = chunk_lines[0]
            last_line = chunk_lines[-1]

            # Build line text formatted with source IDs
            formatted_lines = []
            source_ids = []
            for l in chunk_lines:
                source_ids.append(l.source_id)
                prefix = f"[{l.source_id}]"
                if l.speaker:
                    prefix += f" {l.speaker}:"
                formatted_lines.append(f"{prefix} {l.text}")

            text_representation = "\n".join(formatted_lines)

            window = TranscriptWindow(
                window_id=f"W{window_idx:02d}",
                start_id=first_line.source_id,
                end_id=last_line.source_id,
                start_page=first_line.page,
                start_line=first_line.line,
                end_page=last_line.page,
                end_line=last_line.line,
                source_ids=source_ids,
                lines=chunk_lines,
                text=text_representation
            )
            self.windows.append(window)
            window_idx += 1

            if end_idx == total_substantive:
                break

        return self.windows

    def save_windows(self, output_path: str | Path = "data/processed/processed_windows.json") -> None:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "total_windows": len(self.windows),
            "window_size": self.window_size,
            "overlap": self.overlap,
            "windows": [w.to_dict() for w in self.windows]
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_windows(self, json_path: str | Path = "data/processed/processed_windows.json") -> List[TranscriptWindow]:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.windows = []
        for d in data["windows"]:
            lines = [TranscriptLine.from_dict(l) if isinstance(l, dict) else l for l in d.get("lines", [])]
            w = TranscriptWindow(
                window_id=d["window_id"],
                start_id=d["start_id"],
                end_id=d["end_id"],
                start_page=d["start_page"],
                start_line=d["start_line"],
                end_page=d["end_page"],
                end_line=d["end_line"],
                source_ids=d["source_ids"],
                lines=lines,
                text=d["text"]
            )
            self.windows.append(w)
        return self.windows
