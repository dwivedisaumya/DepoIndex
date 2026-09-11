# Methodology

DepoIndex parses every legal-line slot on printed pages 7–88 into a canonical transcript. Windows preserve each source ID. Candidate detection may use OpenAI when configured or the existing deterministic fallback, but all candidate ranges and every evidence excerpt are checked against the canonical transcript before becoming index data.

Topic segments are chronological occurrences. The threading engine groups semantically matching segments into a topic thread and marks a later occurrence as a re-entry; it never creates one artificial range across an intervening discussion. The integrity auditor reports invalid ranges, text mismatches, duplicate segment IDs, orphan evidence, and long unindexed regions.

## Manual validation protocol

After a run, select at least 20 chronological segments (or all segments if fewer than 20). For each, an attorney records whether location, relevance, boundary quality, coverage, and redundancy are acceptable. Do not calculate a percentage until all observations are recorded. Store the reviewer’s revision separately from the original proposal via the review endpoint.
