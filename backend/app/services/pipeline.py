"""Reproducible end-to-end pipeline and immutable run artifacts."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from .boundary_refiner import TopicBoundaryRefiner
from .chunker import TranscriptChunker
from .exporter import IndexExporter
from .integrity import IndexIntegrityAuditor
from .provenance import ProvenanceValidator
from .reentry_detector import TopicThreadAndReentryEngine
from .topic_detector import CandidateTopicDetector
from .parser import DepositionParser


class DepoIndexPipeline:
    def __init__(self, transcript_path: str | Path | None = None, runs_dir: str | Path | None = None, pdf_path: str | Path | None = None):
        root = Path(__file__).resolve().parents[3]
        self.transcript_path = Path(transcript_path) if transcript_path else root / "data" / "processed" / "processed_transcript.json"
        self.runs_dir = Path(runs_dir) if runs_dir else root / "data" / "runs"
        self.pdf_path = Path(pdf_path) if pdf_path else root / "data" / "raw" / "Persis_Yu_Deposition_Problem_statement.pdf"

    def parse_source(self) -> Dict[str, Any]:
        """Rebuild the canonical artifact from the supplied deposition PDF."""
        parser = DepositionParser(self.pdf_path)
        lines = parser.parse()
        parser.save_canonical(self.transcript_path)
        windows_path = self.transcript_path.with_name("processed_windows.json")
        chunker = TranscriptChunker(lines)
        chunker.create_windows()
        chunker.save_windows(windows_path)
        return {"source_pdf": str(self.pdf_path), "canonical_transcript": str(self.transcript_path), "windows": str(windows_path), "total_slots": len(lines), "non_empty_lines": sum(not line.is_empty for line in lines)}

    def run(self) -> Dict[str, Any]:
        validator = ProvenanceValidator.from_canonical_file(self.transcript_path)
        chunker = TranscriptChunker.from_canonical_file(self.transcript_path)
        windows = chunker.create_windows()
        detector = CandidateTopicDetector(validator)
        candidates = [candidate for window in windows for candidate in detector.detect_candidates_for_window(window)]
        segments = TopicBoundaryRefiner(validator).refine_candidates(candidates)
        threads, segments, relationships = TopicThreadAndReentryEngine().process_threads_and_reentries(segments)
        integrity = IndexIntegrityAuditor(validator).audit(segments, threads).to_dict()
        run_id = f"run_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{uuid4().hex[:8]}"
        run = {"run_id": run_id, "timestamp": datetime.now(timezone.utc).isoformat(), "model": "openai" if detector.openai_api_key else "deterministic-fallback", "number_of_windows": len(windows), "number_of_candidates": len(candidates), "number_of_final_topics": len(segments), "number_of_threads": len(threads), "number_of_reentries": sum(s.is_reentry for s in segments), "coverage_percentage": integrity["coverage_percentage"], "provenance_errors": len(integrity["invalid_references"]) + len(integrity["evidence_mismatches"])}
        payload = IndexExporter().build_payload(segments, threads, relationships, integrity, run)
        folder = self.runs_dir / run_id; folder.mkdir(parents=True, exist_ok=False)
        # Snapshot the immutable source and each decision stage for reproducibility.
        (folder / "parsed_transcript.json").write_text(self.transcript_path.read_text(encoding="utf-8"), encoding="utf-8")
        (folder / "windows.json").write_text(json.dumps({"windows": [w.to_dict() for w in windows]}, indent=2), encoding="utf-8")
        (folder / "candidate_topics.json").write_text(json.dumps([c.to_dict() for c in candidates], indent=2), encoding="utf-8")
        (folder / "refined_topics.json").write_text(json.dumps([s.to_dict() for s in segments], indent=2), encoding="utf-8")
        (folder / "run_metadata.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
        exporter = IndexExporter(); exporter.write_json(payload, folder / "final_index.json"); exporter.write_markdown(payload, folder / "topic_index.md")
        return payload
