from pathlib import Path

import pytest

from backend.app.services.parser import DepositionParser
from backend.app.services.pipeline import DepoIndexPipeline


def test_supported_pdf_factory_rejects_non_pdf(tmp_path):
    source = tmp_path / "not-a-deposition.txt"
    source.write_text("not a PDF", encoding="utf-8")
    with pytest.raises(ValueError, match="PDF"):
        DepositionParser.for_supported_pdf(source)


def test_nonreference_pipeline_uses_supplied_path(tmp_path):
    source = tmp_path / "other.pdf"
    pipeline = DepoIndexPipeline(pdf_path=source, transcript_path=tmp_path / "canonical.json", reference_document=False)
    assert pipeline.pdf_path == source
    assert pipeline.reference_document is False
