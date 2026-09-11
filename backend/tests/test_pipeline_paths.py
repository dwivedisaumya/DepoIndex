from backend.app.services.pipeline import DepoIndexPipeline


def test_pipeline_defaults_are_workspace_absolute_paths():
    pipeline = DepoIndexPipeline()
    assert pipeline.pdf_path.name == "Persis_Yu_Deposition_Problem_statement.pdf"
    assert pipeline.transcript_path.name == "processed_transcript.json"
    assert pipeline.pdf_path.exists()
