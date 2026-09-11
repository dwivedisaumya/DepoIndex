import pytest
from backend.app.services.provenance import ProvenanceValidator

@pytest.fixture
def validator():
    return ProvenanceValidator.from_canonical_file()

def test_valid_reference(validator):
    # Page 11 line 2 to 5 (Question and Answer about attorney background)
    res = validator.validate_reference(11, 2, 11, 5)
    assert res.is_valid is True
    assert res.status == "VERIFIED"
    assert res.start_id == "p11_l02"
    assert res.end_id == "p11_l05"
    assert "attorney" in res.canonical_text.lower()
    assert len(res.source_ids) == 4

def test_invalid_page(validator):
    # Page 200 does not exist
    res = validator.validate_reference(200, 1, 200, 10)
    assert res.is_valid is False
    assert res.status == "PROVENANCE_ERROR"
    assert "out of bounds" in res.error_message

def test_invalid_line(validator):
    # Line 35 does not exist (valid is 1..25)
    res = validator.validate_reference(15, 1, 15, 35)
    assert res.is_valid is False
    assert res.status == "PROVENANCE_ERROR"
    assert "bounds" in res.error_message

def test_reversed_range(validator):
    # End before start
    res = validator.validate_reference(15, 20, 15, 5)
    assert res.is_valid is False
    assert res.status == "PROVENANCE_ERROR"
    assert "Reversed range" in res.error_message

def test_cross_page_range(validator):
    # Span across page boundary: Page 11 line 20 to Page 12 line 5
    res = validator.validate_reference(11, 20, 12, 5)
    assert res.is_valid is True
    assert res.status == "VERIFIED"
    assert res.start_id == "p11_l20"
    assert res.end_id == "p12_l05"
    # Lines: (25 - 20 + 1) + 5 = 6 + 5 = 11
    assert len(res.source_ids) == 11

def test_evidence_matching(validator):
    # Retrieve actual source text for Page 11 line 2 to 3
    source_text = validator.get_source_text(11, 2, 11, 3)
    assert "attorney" in source_text.lower()

    # Valid matching excerpt
    res = validator.validate_reference(11, 2, 11, 3, excerpt="You are an attorney; correct? That is correct.")
    assert res.is_valid is True
    assert res.status == "VERIFIED"
    assert res.matched_excerpt is True

def test_evidence_mismatch(validator):
    # Completely fabricated text
    res = validator.validate_reference(11, 2, 11, 3, excerpt="I was never employed as a lawyer.")
    assert res.is_valid is False
    assert res.status == "PROVENANCE_ERROR"
    assert "does not match" in res.error_message
    assert res.matched_excerpt is False

def test_blank_lines_range(validator):
    # Page 7 lines 1 to 5 are blank preliminary slots
    res = validator.validate_reference(7, 1, 7, 5)
    assert res.is_valid is False
    assert res.status == "PROVENANCE_ERROR"
    assert "blank/unpopulated" in res.error_message
