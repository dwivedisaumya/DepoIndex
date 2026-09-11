from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import pymupdf

from ..models.transcript import TranscriptLine

class DepositionParser:
    """
    High-fidelity provenance-preserving deposition parser.
    Extracts 100% of line coordinates from the certified deposition transcript.
    """

    def __init__(self, pdf_path: str | Path, start_page: int = 7, end_page: int = 88):
        self.pdf_path = Path(pdf_path)
        self.start_page = start_page
        self.end_page = end_page
        self.lines: List[TranscriptLine] = []
        self._line_map: Dict[str, TranscriptLine] = {}
        self._coord_map: Dict[Tuple[int, int], TranscriptLine] = {}

    @classmethod
    def for_supported_pdf(cls, pdf_path: str | Path) -> "DepositionParser":
        """Create a parser for another text-based, 25-line legal transcript.

        This deliberately accepts only the layout this parser can preserve with
        legal page/line fidelity.  It never substitutes the reference PDF.
        """
        path = Path(pdf_path)
        if not path.exists() or path.suffix.lower() != ".pdf":
            raise ValueError("Unsupported input: provide an existing PDF file.")
        try:
            doc = pymupdf.open(path)
        except Exception as exc:
            raise ValueError("Unsupported input: PDF is corrupted or cannot be opened.") from exc
        structured_pages = []
        for page_number in range(1, doc.page_count + 1):
            blocks = doc[page_number - 1].get_text("blocks")
            slots = set()
            for block in blocks:
                match = re.match(r"^(\d{1,2})(?:\n.*)?$", block[4].strip(), re.DOTALL)
                if match and 1 <= int(match.group(1)) <= 25:
                    slots.add(int(match.group(1)))
            if len(slots) >= 10:
                structured_pages.append(page_number)
        if not structured_pages:
            raise ValueError("Unsupported input: no text-based numbered legal transcript pages were found (OCR is not supported).")
        expected_pages = list(range(min(structured_pages), max(structured_pages) + 1))
        if structured_pages != expected_pages:
            raise ValueError("Unsupported input: numbered transcript pages are not a continuous legal-transcript range.")
        return cls(path, start_page=min(structured_pages), end_page=max(structured_pages))

    def parse(self) -> List[TranscriptLine]:
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Deposition PDF not found at {self.pdf_path}")

        doc = pymupdf.open(self.pdf_path)
        extracted: List[TranscriptLine] = []

        current_speaker: Optional[str] = None

        for page_no in range(self.start_page, self.end_page + 1):
            page_idx = page_no - 1
            if page_idx >= doc.page_count:
                break

            page = doc[page_idx]
            blocks = page.get_text("blocks")

            # Collect line blocks on this page
            page_line_slots: Dict[int, str] = {i: "" for i in range(1, 26)}

            for b in blocks:
                btext = b[4].strip()
                # Format: line number followed by text
                # e.g. "1\n  BY MR. PURCELL:                                              01:20"
                m = re.match(r"^(\d{1,2})(?:\n(.*))?$", btext, re.DOTALL)
                if m:
                    lno = int(m.group(1))
                    if 1 <= lno <= 25:
                        page_line_slots[lno] = m.group(2).strip() if m.group(2) else ""

            # Build canonical TranscriptLine for every slot 1..25
            for lno in range(1, 26):
                raw_slot = page_line_slots[lno]
                source_id = f"p{page_no:02d}_l{lno:02d}"

                if not raw_slot:
                    t_line = TranscriptLine(
                        source_id=source_id,
                        page=page_no,
                        line=lno,
                        text="",
                        raw_text="",
                        speaker=None,
                        timestamp=None,
                        is_empty=True
                    )
                    extracted.append(t_line)
                    continue

                # Separate trailing timestamp if present (e.g. "01:20")
                timestamp = None
                text_body = raw_slot
                ts_match = re.search(r"\b(\d{2}:\d{2})\s*$", raw_slot)
                if ts_match:
                    timestamp = ts_match.group(1)
                    text_body = raw_slot[:ts_match.start()].strip()

                # Detect speaker tags and Q/A markers
                speaker = None
                is_q = False
                is_a = False
                is_colloquy = False

                # Speaker patterns
                if re.match(r"^BY\s+MR\.\s+PURCELL:", text_body, re.I):
                    speaker = "MR. PURCELL"
                    is_colloquy = True
                    # Clean prefix
                    text_body = re.sub(r"^BY\s+MR\.\s+PURCELL:\s*", "", text_body, flags=re.I).strip()
                elif re.match(r"^MR\.\s+PURCELL:", text_body, re.I):
                    speaker = "MR. PURCELL"
                    is_colloquy = True
                    text_body = re.sub(r"^MR\.\s+PURCELL:\s*", "", text_body, flags=re.I).strip()
                elif re.match(r"^MR\.\s+BLOOD:", text_body, re.I):
                    speaker = "MR. BLOOD"
                    is_colloquy = True
                    text_body = re.sub(r"^MR\.\s+BLOOD:\s*", "", text_body, flags=re.I).strip()
                elif re.match(r"^THE\s+WITNESS:", text_body, re.I):
                    speaker = "THE WITNESS"
                    is_a = True
                    text_body = re.sub(r"^THE\s+WITNESS:\s*", "", text_body, flags=re.I).strip()
                elif re.match(r"^THE\s+VIDEOGRAPHER:", text_body, re.I):
                    speaker = "THE VIDEOGRAPHER"
                    is_colloquy = True
                    text_body = re.sub(r"^THE\s+VIDEOGRAPHER:\s*", "", text_body, flags=re.I).strip()
                elif re.match(r"^THE\s+REPORTER:", text_body, re.I):
                    speaker = "THE REPORTER"
                    is_colloquy = True
                    text_body = re.sub(r"^THE\s+REPORTER:\s*", "", text_body, flags=re.I).strip()
                elif re.match(r"^Q\b\.?", text_body):
                    speaker = "Q"
                    is_q = True
                    text_body = re.sub(r"^Q\b\.?\s*", "", text_body).strip()
                elif re.match(r"^A\b\.?", text_body):
                    speaker = "A"
                    is_a = True
                    text_body = re.sub(r"^A\b\.?\s*", "", text_body).strip()
                else:
                    # Inherit current active speaker for multi-line flow if appropriate
                    pass

                # Track active speaker context
                if speaker:
                    current_speaker = speaker

                t_line = TranscriptLine(
                    source_id=source_id,
                    page=page_no,
                    line=lno,
                    text=text_body,
                    raw_text=raw_slot,
                    speaker=speaker or current_speaker,
                    timestamp=timestamp,
                    is_question=is_q,
                    is_answer=is_a,
                    is_colloquy=is_colloquy,
                    is_empty=False
                )
                extracted.append(t_line)

        self.lines = extracted
        self._line_map = {l.source_id: l for l in extracted}
        self._coord_map = {(l.page, l.line): l for l in extracted}
        return self.lines

    def save_canonical(self, output_path: str | Path) -> None:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "source_pdf": str(self.pdf_path),
            "start_page": self.start_page,
            "end_page": self.end_page,
            "total_slots": len(self.lines),
            "non_empty_lines": sum(1 for l in self.lines if not l.is_empty),
            "lines": [l.to_dict() for l in self.lines]
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_canonical(self, json_path: str | Path) -> List[TranscriptLine]:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.lines = [TranscriptLine.from_dict(d) for d in data["lines"]]
        self._line_map = {l.source_id: l for l in self.lines}
        self._coord_map = {(l.page, l.line): l for l in self.lines}
        return self.lines

    def get_line(self, source_id: str) -> Optional[TranscriptLine]:
        return self._line_map.get(source_id)

    def get_by_coord(self, page: int, line: int) -> Optional[TranscriptLine]:
        return self._coord_map.get((page, line))

    def get_range(self, start_page: int, start_line: int, end_page: int, end_line: int) -> List[TranscriptLine]:
        """Return slice of lines between coordinates inclusive."""
        result: List[TranscriptLine] = []
        for l in self.lines:
            if (l.page, l.line) < (start_page, start_line):
                continue
            if (l.page, l.line) > (end_page, end_line):
                break
            result.append(l)
        return result
