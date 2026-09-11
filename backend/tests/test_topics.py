import pytest
from backend.app.services.parser import DepositionParser
from backend.app.services.provenance import ProvenanceValidator
from backend.app.services.chunker import TranscriptChunker
from backend.app.services.topic_detector import CandidateTopicDetector
from backend.app.services.boundary_refiner import TopicBoundaryRefiner
from backend.app.services.reentry_detector import TopicThreadAndReentryEngine
from backend.app.services.topic_detector import CandidateTopic

@pytest.fixture(scope="module")
def pipeline_components():
    validator = ProvenanceValidator.from_canonical_file()
    chunker = TranscriptChunker.from_canonical_file(window_size=50, overlap=10)
    windows = chunker.create_windows()
    detector = CandidateTopicDetector(validator)
    refiner = TopicBoundaryRefiner(validator)
    reentry_engine = TopicThreadAndReentryEngine()
    return validator, windows, detector, refiner, reentry_engine

def test_candidate_detection_and_refinement(pipeline_components):
    validator, windows, detector, refiner, reentry_engine = pipeline_components

    # Detect candidates for first 5 windows
    candidates = []
    for w in windows[:8]:
        cands = detector.detect_candidates_for_window(w)
        candidates.extend(cands)

    assert len(candidates) > 0

    # Refine boundaries
    segments = refiner.refine_candidates(candidates)
    assert len(segments) > 0

    # Verify every refined segment strictly passes provenance validation
    for s in segments:
        val = validator.validate_reference(s.start_page, s.start_line, s.end_page, s.end_line)
        assert val.is_valid is True, f"Segment {s.segment_id} ({s.title}) failed validation: {val.error_message}"
        assert val.status == "VERIFIED"
        assert len(s.evidence) > 0
        assert s.evidence[0].verification_status == "verified"

def test_full_deposition_topic_threading_and_reentry(pipeline_components):
    validator, windows, detector, refiner, reentry_engine = pipeline_components

    # Process all 51 windows of the complete deposition
    all_candidates = []
    for w in windows:
        cands = detector.detect_candidates_for_window(w)
        all_candidates.extend(cands)

    assert len(all_candidates) >= len(windows)

    # Refine into segments
    segments = refiner.refine_candidates(all_candidates)
    assert len(segments) >= 15, f"Expected at least 15 topic segments, got {len(segments)}"

    # Thread and re-entry detection
    threads, threaded_segments, relationships = reentry_engine.process_threads_and_reentries(segments)

    assert len(threads) > 0
    assert len(threaded_segments) == len(segments)
    assert len(relationships) > 0

    # Check for re-entries
    reentries = [s for s in threaded_segments if s.is_reentry]
    print(f"Total topics: {len(threaded_segments)}, Threads: {len(threads)}, Re-entries: {len(reentries)}")
    assert len(reentries) > 0, "Expected at least one re-entry across the 82 pages of testimony"

    # Verify relationships include both 'continues' and 're-enters'
    rel_types = {r.relationship_type for r in relationships}
    assert "continues" in rel_types
    assert "re-enters" in rel_types

    # Verify chronological ordering
    for i in range(len(threaded_segments) - 1):
        s1 = threaded_segments[i]
        s2 = threaded_segments[i + 1]
        assert (s1.start_page, s1.start_line) <= (s2.start_page, s2.start_line), f"Ordering error between {s1.segment_id} and {s2.segment_id}"

def test_llm_candidate_with_invented_evidence_id_is_rejected(pipeline_components):
    validator, windows, detector, *_ = pipeline_components
    window = windows[0]
    invented = CandidateTopic("Test", "test", window.start_page, window.start_line, window.end_page, window.end_line, ["p99_l99"])
    assert detector._validate_and_filter_candidates([invented], window) == []
