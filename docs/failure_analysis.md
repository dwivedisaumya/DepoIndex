# DepoIndex — Failure Analysis

**Project:** DepoIndex  
**Source transcript:** Persis Yu deposition  
**Index:** Topic Index  
**Prepared by:** SAUMYA DWIVEDI  
**Date:** 13/09/2026

---

# Failure Case Analysis

The following cases were identified during manual validation of the
supplied DepoIndex Topic Index.

The cases focus on genuine weaknesses in topic labeling and segmentation.
The previously suspected systemic +1 page offset is not included because
re-verification against the actual Persis Yu PDF showed that the generated
page/line coordinates are correct.

---

# Failure Case 1 — Topic Label Mismatch

## Entry

**Entry 16 — Run 1**

Topic label:

`ITT Technical Institute & For-Profit Lending`

Citation:

`p. 26:15–p. 27:9`

## What Went Wrong?

The cited testimony is primarily a housekeeping / report paragraph-numbering
exchange rather than substantive ITT or for-profit-lending testimony.

The generated location is correct, but the topic label does not accurately
describe the cited span.

## What Should Have Happened?

The entry should either:

- use a label describing the report/paragraph-numbering discussion, or
- be merged into the surrounding topic if the exchange does not represent
  a meaningful independent subject.

## Why Did It Fail?

The topic-label generation appears to be influenced by broader surrounding
context rather than being strictly grounded in the final citation span.

## Impact

An attorney searching for ITT-related testimony could be directed to an
irrelevant housekeeping exchange.

## How to Fix

1. Generate labels only from the final evidence span.
2. Require the model to justify the label using the cited text.
3. Use a controlled topic vocabulary where appropriate.
4. Reject labels whose key subject is not supported by the citation.

---

# Failure Case 2 — Nested Topic Range

## Entry

**Entry 13 inside Entry 12**

Entry 12:

`p. 19:15–p. 24:4`

Entry 13:

`p. 23:19–p. 23:22`

## What Went Wrong?

Entry 13 is completely contained inside Entry 12.

Although the cited location itself is correct, the same broader testimony is
claimed by two Topic Index entries.

## What Should Have Happened?

If the short PEAKS/ITT exchange represents a genuine independent topic, the
boundary should be explicitly redrawn so that the ranges do not nest
unnecessarily.

Otherwise, it should remain part of the larger loan-servicing topic.

## Why Did It Fail?

The segmentation stage can create a new topic from a short exchange without
checking whether its range is already contained inside a neighboring topic.

## Impact

This creates redundant navigation and makes it unclear whether both rows
should be treated as independent topics.

## How to Fix

Add a post-processing stage that:

- detects nested ranges,
- checks whether the subject matter actually changes,
- merges redundant entries,
- redraws boundaries when necessary.

---

# Failure Case 3 — Overlapping Topic Ranges

## Entries

**Entries 19 and 20**

Entry 19:

`p. 37:16–p. 38:6`

Entry 20:

`p. 37:19–p. 42:3`

## What Went Wrong?

The two citation ranges overlap from:

`p. 37:19–p. 38:6`

The same testimony is therefore claimed by both entries.

## What Should Have Happened?

The system should establish one clean boundary between the two topics unless
the overlapping testimony is explicitly justified as belonging to both.

For a chronological Topic Index, duplicate ownership of the same testimony
should generally be avoided.

## Why Did It Fail?

Topic boundary detection and post-processing do not currently enforce
non-overlapping chronological ranges.

## Impact

An attorney following the Topic Index may encounter duplicate testimony
and uncertainty about which topic owns the passage.

## How to Fix

Add automated overlap detection after topic generation.

When two ranges overlap:

1. Compare their subject matter.
2. Merge them if they represent the same topic.
3. Otherwise redraw the boundary at the actual subject-matter transition.
4. Reject unresolved overlapping ranges.

---

# Additional Observed Boundary Issue — Lead-In Lines

Several entries begin on `BY MR. PURCELL` lead-in lines.

These locations are technically correct because they correspond to the exact
numbered transcript blocks.

However, the first substantive testimony may begin on the following line.

This is therefore a **boundary-quality issue rather than a location-accuracy
failure**.

A future refinement could prefer the first substantive testimony line while
preserving the exact transcript coordinate.

---

# Root-Cause Summary

The observed weaknesses are concentrated in:

1. Evidence-grounded topic labeling
2. Topic segmentation granularity
3. Overlap / nested-range handling
4. Boundary post-processing

The source-location mechanism itself performed correctly for the tested
Persis Yu PDF.

---

# Corrective Actions

## 1. Evidence-Grounded Labels

Generate labels strictly from the final citation span.

## 2. Boundary Detection

Use subject-matter transitions rather than merely short question/answer
changes.

## 3. Overlap Detection

Automatically identify overlapping and nested page/line ranges.

## 4. Merge / De-duplication

Merge short fragments when they do not represent meaningful independent
topics.

## 5. Minimum Span Rule

Introduce a minimum span or minimum semantic-distinctness requirement before
creating a new Topic Index entry.

## 6. Provenance Validation

Continue validating every generated citation against the original transcript.

---

# Overall Conclusion

The validation shows that DepoIndex's primary current weaknesses are not
page-location errors but **topic labeling and segmentation quality**.

The 20 sampled citations were correctly mapped to the actual Persis Yu PDF.
The remaining failures concern whether a cited span deserves its own topic
and whether neighboring topics should overlap or nest.

The prototype therefore requires stronger evidence-grounded labeling and
boundary post-processing before it can be considered reliable for
unsupervised professional use.
