from backend.app.models.evidence import EvidenceItem
from backend.app.models.topic import TopicConfidence, TopicSegment
from backend.app.services.exporter import IndexExporter
from backend.app.services.integrity import IndexIntegrityAuditor
from backend.app.services.provenance import ProvenanceValidator


def verified_segment():
    evidence = EvidenceItem("ev1", 11, 2, 11, 3, "p11_l02", "p11_l03", ["p11_l02", "p11_l03"], "You are an attorney; correct? That is correct.", "p. 11:2–3")
    return TopicSegment("S01A", "TT01", "T01", "Attorney Background", "Attorney qualification testimony.", 11, 2, 11, 3, "p11_l02", "p11_l03", [evidence], confidence=TopicConfidence())


def test_integrity_reports_verified_evidence():
    report = IndexIntegrityAuditor(ProvenanceValidator.from_canonical_file()).audit([verified_segment()])
    assert report.invalid_references == []
    assert report.evidence_mismatches == []
    assert report.covered_lines == 2


def test_export_contains_citations(tmp_path):
    segment = verified_segment()
    payload = IndexExporter().build_payload([segment], [], [], {"healthy": True}, {"run_id": "test"})
    output = IndexExporter().write_markdown(payload, tmp_path / "index.md")
    assert "p. 11:2" in output.read_text(encoding="utf-8")
