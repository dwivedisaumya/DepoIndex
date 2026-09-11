"""Durable, non-destructive attorney-review storage using the standard library."""
from __future__ import annotations
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

class ReviewStore:
    def __init__(self, database_path: str | Path = "data/depoindex.db"):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS attorney_reviews (review_id TEXT PRIMARY KEY, segment_id TEXT NOT NULL, run_id TEXT NOT NULL, status TEXT NOT NULL, original_proposal TEXT NOT NULL, revision TEXT NOT NULL, reviewed_by TEXT NOT NULL, created_at TEXT NOT NULL)""")

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def save(self, segment_id: str, run_id: str, status: str, original_proposal: Dict[str, Any], revision: Dict[str, Any], reviewed_by: str = "Attorney Reviewer") -> Dict[str, Any]:
        record = {"review_id": str(uuid4()), "segment_id": segment_id, "run_id": run_id, "status": status, "original_proposal": original_proposal, "revision": revision, "reviewed_by": reviewed_by, "created_at": datetime.now(timezone.utc).isoformat()}
        with self._connect() as connection:
            connection.execute("INSERT INTO attorney_reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (record["review_id"], record["segment_id"], record["run_id"], record["status"], json.dumps(record["original_proposal"]), json.dumps(record["revision"]), record["reviewed_by"], record["created_at"]))
        return record

    def list_for_segment(self, segment_id: str) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute("SELECT review_id, segment_id, run_id, status, original_proposal, revision, reviewed_by, created_at FROM attorney_reviews WHERE segment_id = ? ORDER BY created_at DESC", (segment_id,)).fetchall()
        keys = ("review_id", "segment_id", "run_id", "status", "original_proposal", "revision", "reviewed_by", "created_at")
        return [{**dict(zip(keys, row)), "original_proposal": json.loads(row[4]), "revision": json.loads(row[5])} for row in rows]
