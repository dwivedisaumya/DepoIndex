from backend.app.services.review_store import ReviewStore


def test_review_preserves_original_proposal(tmp_path):
    store = ReviewStore(tmp_path / "reviews.db")
    original = {"segment_id": "S01A", "title": "AI proposal"}
    saved = store.save("S01A", "run_1", "EDITED", original, {"revised_title": "Attorney title"}, "A. Reviewer")
    assert saved["original_proposal"] == original
    assert store.list_for_segment("S01A")[0]["revision"]["revised_title"] == "Attorney title"
