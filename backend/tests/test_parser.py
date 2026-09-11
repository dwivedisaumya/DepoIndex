import pytest
from pathlib import Path
from backend.app.services.parser import DepositionParser
from backend.app.models.transcript import TranscriptLine

PDF_PATH = Path("data/raw/Persis_Yu_Deposition_Problem_statement.pdf")
JSON_PATH = Path("data/processed/processed_transcript.json")

def test_parser_file_exists():
    assert PDF_PATH.exists(), f"Source PDF missing at {PDF_PATH}"

def test_parse_complete_deposition():
    parser = DepositionParser(PDF_PATH, start_page=7, end_page=88)
    lines = parser.parse()

    # Total line slots should be 82 pages * 25 lines = 2050
    assert len(lines) == 2050
    assert parser.lines == lines

    # Verify line indexing continuity
    for idx, line in enumerate(lines):
        expected_page = 7 + (idx // 25)
        expected_line = 1 + (idx % 25)
        expected_source_id = f"p{expected_page:02d}_l{expected_line:02d}"

        assert line.page == expected_page, f"Line {idx} page mismatch: {line.page} vs {expected_page}"
        assert line.line == expected_line, f"Line {idx} line mismatch: {line.line} vs {expected_line}"
        assert line.source_id == expected_source_id

def test_saved_canonical_transcript_integrity():
    assert JSON_PATH.exists(), "processed_transcript.json does not exist"
    parser = DepositionParser(PDF_PATH)
    lines = parser.load_canonical(JSON_PATH)

    assert len(lines) == 2050
    non_empty = [l for l in lines if not l.is_empty]
    assert len(non_empty) == 2032

    # Verify Page 7 starts examination on line 11
    p7_l11 = parser.get_line("p07_l11")
    assert p7_l11 is not None
    assert "PURCELL" in (p7_l11.speaker or "")

    # Verify Page 11 Q&A structure
    p11_l02 = parser.get_line("p11_l02")
    assert p11_l02 is not None
    assert p11_l02.is_question is True
    assert "attorney" in p11_l02.text.lower()

    p11_l03 = parser.get_line("p11_l03")
    assert p11_l03 is not None
    assert p11_l03.is_answer is True
    assert "correct" in p11_l03.text.lower()

    # Verify Page 88 deposition conclusion on line 17
    p88_l17 = parser.get_line("p88_l17")
    assert p88_l17 is not None
    assert "concluded" in p88_l17.text.lower() or "concluded" in p88_l17.raw_text.lower()

def test_get_range_functionality():
    parser = DepositionParser(PDF_PATH)
    parser.load_canonical(JSON_PATH)

    # Range spanning single page: p10_l01 to p10_l25
    r1 = parser.get_range(10, 1, 10, 25)
    assert len(r1) == 25
    assert r1[0].source_id == "p10_l01"
    assert r1[-1].source_id == "p10_l25"

    # Range spanning across page boundaries: p10_l20 to p11_l05
    r2 = parser.get_range(10, 20, 11, 5)
    assert len(r2) == 11  # (25 - 20 + 1) + 5 = 6 + 5 = 11 lines
    assert r2[0].source_id == "p10_l20"
    assert r2[-1].source_id == "p11_l05"
