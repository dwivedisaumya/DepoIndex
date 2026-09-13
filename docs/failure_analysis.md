# DepoIndex — Failure Analysis

**Project:** DepoIndex  
**Source transcript:** Persis Yu deposition  
**Index:** Topic Index  
**Prepared by:** SAUMYA DWIVEDI  
**Date:** 13/09/2026

---

# Failure Case Analysis

This report documents three observed failure cases from the manual validation of the supplied DepoIndex Topic Index output.

The failures are based on actual reviewed entries and are not hypothetical examples.

The three cases cover:

1. A systemic page-location error
2. Topic-label hallucination / mismatch with cited evidence
3. Over-segmentation, overlap, and nested citation ranges

---

# Failure Case 1 — Systemic +1 Page Offset

## Entry / Topic / Run

**All 20 reviewed entries — Run 1 / the only generated run**

---

## What Went Wrong?

Every single page citation is off by exactly **+1 page** versus the real transcript.

For example, an index citation beginning on p. 7 corresponds to testimony that actually begins on p. 6 of the real transcript.

This occurred consistently across all 20 manually reviewed entries.

---

## Why Did It Happen?

The observed behavior indicates a page-indexing bug in extraction.

The most likely cause is that an extra cover/caption or exhibit page was counted into the running "Page N" label, shifting every subsequent reference by one page for the rest of the document.

---

## Impact

An attorney opening any cited page would land one page after the actual testimony, every single time.

This fails the assignment's own bar:

> A plausible label with the wrong location is a failure.

Therefore, this is not a small isolated citation problem. It affects the location accuracy of **all 20 sampled entries**.

A topic index whose locations consistently point to the wrong page cannot reliably serve its primary navigation and verification purpose.

---

## How to Fix

1. Derive page numbers directly from the transcript's own printed `"Page N"` stamps / line-number column instead of a separately counted physical-page index.

2. Add an automated citation verifier that re-locates each entry's quoted evidence in the source text.

3. Reject the entry if the returned page/line does not match the citation stored in the index.

This would make citation correctness an explicit validation step rather than relying on the extraction page counter.

---

## Evidence / Citation

The systemic offset was independently verified at three widely separated points:

- Real p. 6 vs. claimed p. 7 — opening admonitions
- Real p. 46 vs. claimed p. 47 — CFPB settlement order testimony
- Real p. 86 vs. claimed p. 87 — PEAKS investigations near the end

The constant offset was observed across the approximately 91-page transcript.

---

# Failure Case 2 — Topic Label Does Not Match Cited Testimony

## Entry / Topic / Run

**Entries 5, 6 and 16 — Run 1**

- Entry 5: `"PEAKS Loan Unenforceability & 2020 Settlement"`
- Entry 6: `"ITT Technical Institute & For-Profit Lending"`
- Entry 16: `"ITT Technical Institute & For-Profit Lending"`

---

## What Went Wrong?

The topic labels do not match the cited testimony.

### Entry 5

Entry 5 is labeled:

**PEAKS Loan Unenforceability & 2020 Settlement**

However, its actual cited testimony is the witness describing SBPC's general policy-advocacy agenda.

Nothing about PEAKS loan unenforceability or the 2020 settlement appears in the cited span.

### Entry 6

Entry 6 is labeled:

**ITT Technical Institute & For-Profit Lending**

However, the actual cited testimony is still SBPC's general policy-initiative work and borrower protections.

The cited span is not ITT-specific or substantive for-profit-lending testimony.

### Entry 16

Entry 16 is also labeled:

**ITT Technical Institute & For-Profit Lending**

However, the actual testimony is a housekeeping question about paragraph numbering in the expert report.

Nothing about ITT or for-profit lending appears in the cited span.

---

## Why Did It Happen?

The behavior appears consistent with topic-label generation drawing on a wider or summarized context window rather than being grounded strictly in the exact quoted span.

A nearby high-salience keyword such as `"ITT"` or `"PEAKS"` may have influenced the label even though that subject was not actually discussed in the cited evidence.

This represents a classic hallucination risk when label generation and citation extraction are not tightly coupled to the same evidence.

---

## Impact

This is worse than a missing entry because the index can confidently direct an attorney to unrelated testimony.

For example, an attorney searching for:

**"PEAKS Loan Unenforceability"**

could be directed to SBPC advocacy testimony that does not contain the requested subject.

The user could therefore miss the actual PEAKS/settlement discussion elsewhere in the transcript while trusting that the index has already located it.

This undermines trust in the index.

---

## How to Fix

1. Generate the topic label only from the small quoted span backing the citation.

2. Require a self-check step where the model must justify the topic label using solely the quoted text.

3. Constrain labels to a controlled topic vocabulary where appropriate.

4. Use a taxonomy derived from the case's exhibit list, complaint, or issues list.

5. Require the model to explicitly justify any deviation from the controlled vocabulary.

The central requirement is that the label must be grounded in the exact evidence used for the citation.

---

## Evidence / Citation

Entry 5's actual cited testimony on real p. 11 includes discussion of:

- Issues related to the student loan safety net
- Adequate protections for federal student loan borrowers
- Issues of racial equity

There is no PEAKS or settlement language anywhere in the cited span.

---

# Failure Case 3 — Over-Segmentation, Overlap, and Nested Ranges

## Entry / Topic / Run

**Run 1**

Affected entries include:

- Entries 10, 13 and 17, which are nested inside neighboring entries.
- Entries 4/5
- Entries 6/7
- Entries 19/20

The latter pairs contain overlapping citation ranges.

---

## What Went Wrong?

Three entries are fully contained within a neighboring entry's page/line range.

This means the same testimony is claimed by more than one Topic Index row.

Three adjacent pairs also overlap by several lines each.

Therefore, the segmentation contains both:

- **Nested ranges**
- **Overlapping ranges**

---

## Why Did It Happen?

The segmentation behavior appears to fire a "new topic" on a question/answer pair with slightly different surface phrasing, such as a clarifying question, rather than requiring a genuine subject-matter shift.

Boundary detection also appears to operate somewhat independently of labeling.

As a result:

- A short aside can become a new topic.
- A generic label can be assigned to that aside.
- The new entry receives its own citation range.
- The underlying topic has not actually changed.

This produces fragmentation of what should remain one continuous topic.

---

## Impact

The result is fragmented and redundant navigation.

An attorney following the index can be bounced between overlapping rows for what is actually one continuous answer.

This:

- Wastes review time.
- Makes the index harder to navigate.
- Reduces confidence in the topic boundaries.
- Creates uncertainty about which entry should be treated as authoritative.

---

## How to Fix

1. Add a minimum-span / merge rule.

2. Fold any candidate topic shorter than a defined number of lines into its neighbor unless it is genuinely a distinct subject.

3. Add a post-processing pass that detects overlapping citation ranges.

4. Detect nested citation ranges automatically.

5. Merge overlapping or nested ranges where the subject matter has not actually changed.

6. Force the model to redraw a single clean boundary when two entries claim the same testimony.

---

## Evidence / Citation

### Entry 13 nested inside Entry 12

- Entry 12: p. 19:15–p. 24:4
- Entry 13: p. 23:19–p. 23:22

Entry 13 sits entirely inside Entry 12's range.

The actual topic does not change at that point. The 4-line segment is an aside within the broader loan-servicing-transfer discussion.

---

### Entry 17 nested inside Entry 16

- Entry 16: p. 26:15–p. 27:9
- Entry 17: p. 26:20–p. 27:1

Entry 17 is entirely contained inside Entry 16.

The two entries are part of the same exchange and should be merged rather than treated as independent topics.

---

### Entries 19 and 20 overlap

- Entry 19 ends at p. 38:6.
- Entry 20 begins at p. 37:19.

This creates a **3-line overlap**.

The same testimony is therefore claimed by both entries.

---

# Overall Failure-Analysis Conclusion

The three observed failure cases show that the main weaknesses are concentrated in three parts of the indexing pipeline:

1. **Citation extraction / page indexing**
2. **Evidence-grounded topic labeling**
3. **Topic segmentation and boundary post-processing**

The most severe systemic issue is the **+1 page offset**, because it affects every sampled citation.

The topic-label mismatch is also serious because it can confidently direct an attorney to unrelated testimony.

The overlap and nesting problem reduces navigation quality and indicates that topic segmentation requires a stronger merge/de-duplication stage.

Together, these issues support the overall assessment that DepoIndex is **PROTOTYPE-STAGE** and is not yet production-ready for unsupervised attorney use.

---

# Relevant Corrective Actions

## 1. Fix Page Indexing

Derive page numbers directly from the transcript's embedded `"Page N"` markers rather than a separately counted physical-page index.

Add an automated citation verifier that re-locates each entry's quoted evidence and rejects citations whose page/line location does not align.

---

## 2. Couple Evidence, Boundaries, and Labels

First detect candidate topic boundaries from the raw transcript.

Possible signals include:

- Embedding-similarity shifts
- Discourse markers such as `"Let's move to..."`

Then generate the topic label strictly from the text inside that boundary.

This reduces the chance that a label will be generated from unrelated surrounding context.

---

## 3. Add Merge / De-duplication

Add a post-processing stage that:

- Applies a minimum line/span threshold.
- Folds very short fragments into neighboring topics when appropriate.
- Detects overlapping ranges.
- Detects nested ranges.
- Merges or redraws boundaries where the subject matter has not actually changed.

---

## 4. Run Controlled Stability Tests

Run the actual pipeline three or more times using:

- Temperature 0
- Fixed/deterministic chunking
- Logged topic counts
- Logged labels
- Logged citations

This would provide genuine automated stability metrics instead of the manual proxy used in the current validation.

---

## 5. Introduce a Controlled Topic Taxonomy

Introduce a controlled or suggested topic taxonomy derived from the case's:

- Exhibit list
- Complaint
- Issues list

The model should select from the taxonomy or explicitly justify a deviation.

This is intended to reduce label hallucination of the type observed in Entries 5, 6, and 16.
