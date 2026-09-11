"""Verified JSON and human-readable exports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from ..models.topic import TopicRelationship, TopicSegment, TopicThread


class IndexExporter:
    def build_payload(self, segments: Iterable[TopicSegment], threads: Iterable[TopicThread], relationships: Iterable[TopicRelationship], integrity: Dict[str, Any], run: Dict[str, Any]) -> Dict[str, Any]:
        return {"run": run, "threads": [t.to_dict() for t in threads], "segments": [s.to_dict() for s in segments], "relationships": [r.to_dict() for r in relationships], "integrity": integrity}

    def write_json(self, payload: Dict[str, Any], path: str | Path) -> Path:
        target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return target

    def write_markdown(self, payload: Dict[str, Any], path: str | Path) -> Path:
        target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
        rows = ["# DepoIndex Topic Index", "", "## Chronological segments", ""]
        for segment in payload["segments"]:
            rows += [f"### {segment['title']}", f"**Citation:** p. {segment['start_page']}:{segment['start_line']}–p. {segment['end_page']}:{segment['end_line']}", "", segment["description"], ""]
            for evidence in segment.get("evidence", []):
                rows.append(f"> {evidence['citation']}: {evidence['text']}")
        target.write_text("\n".join(rows) + "\n", encoding="utf-8")
        return target
