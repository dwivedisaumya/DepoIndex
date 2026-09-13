# DepoIndex — Validation Report

**Project:** DepoIndex  
**Source transcript:** Persis Yu deposition  
**Index:** Topic Index  
**Prepared by:** SAUMYA DWIVEDI  
**Date:** 13/09/2026

---

# 1. Evaluation Methodology

The DepoIndex Topic Index was manually evaluated against the supplied
`Persis_Yu_Deposition_Problem_statement.pdf`.

A total of **20 Topic Index entries** were reviewed.

Each entry was evaluated on:

1. **Location Accuracy** — whether the generated start and end page/line
   references correspond to the actual numbered transcript blocks.

2. **Topic Relevance** — whether the topic label accurately describes the
   cited testimony.

3. **Boundary Quality** — whether the selected start and end boundaries
   represent a reasonable subject-matter span.

4. **Coverage** — whether important subject areas in the reviewed range
   were represented.

5. **Redundancy** — whether unnecessary duplicate, overlapping, or nested
   topics were generated.

The location verification was re-checked against the actual repository copy
of the Persis Yu PDF.

---

# 2. Location Accuracy

## Result: PASS

The 20 sampled citations were re-verified against the actual Persis Yu PDF.

The source PDF contains administrative pages 1–4 without transcript footers.
Beginning with physical page 5, the printed transcript page number matches
the physical PDF page number through the checked range.

The parser converts the physical page number to a zero-based PDF array index
only for PDF access, while preserving the one-based page number as the
canonical citation coordinate.

Therefore, the generated page references are not affected by a systemic
+1 page conversion error.

### 20-Entry Result

| Metric | Result |
|---|---:|
| Correct locations | 20/20 |
| Partial | 0/20 |
| Incorrect | 0/20 |
| Location Accuracy | **100%** |

The four entries whose boundaries begin on `BY MR. PURCELL` lead-in lines still
point to the exact PDF line. These may be boundary-quality considerations,
but they are not page or line-location errors.

---

# 3. Topic Relevance

## Result: MIXED

The major subject areas are generally identifiable from the generated
Topic Index.

However, some entries use labels that are broader or more specific than
the testimony contained in the cited span.

For example, some entries labelled as ITT-related or deposition-testimony
topics cover short exchanges, housekeeping questions, or surrounding
testimony rather than a clean standalone topic.

This indicates that topic labeling is directionally useful but still needs
stronger evidence grounding.

### Main Issue

Topic labels should be generated from the exact evidence contained inside
the final citation range rather than from a wider surrounding context.

---

# 4. Boundary Quality

## Result: MIXED

The generated boundaries are often usable, but several entries demonstrate
overlapping or nested ranges.

Examples include:

- Entry 13 is contained within Entry 12.
- Entry 17 is contained within Entry 16.
- Entries 19 and 20 overlap.

These cases indicate that the system can identify relevant subject matter
but does not always establish a single clean boundary between neighboring
topics.

---

# 5. Coverage

## Result: GENERALLY GOOD

The reviewed Topic Index covers the major subject areas appearing in the
reviewed transcript range, including:

- Deposition formalities
- Witness background and curriculum vitae
- Student Borrower Protection Center advocacy
- Student loan servicing and transfers
- PEAKS / Vervent-related testimony
- ITT Technical Institute and for-profit lending
- CFPB investigations and enforcement

The main coverage limitation is therefore not a major missing-topic
problem, but rather how finely the system divides related testimony.

---

# 6. Redundancy

## Result: NEEDS IMPROVEMENT

The Topic Index contains overlapping and nested entries.

This causes some testimony to be represented by more than one Topic Index
row.

Examples:

- Entry 13 is nested inside Entry 12.
- Entry 17 is nested inside Entry 16.
- Entries 19 and 20 have an overlapping citation range.

A post-processing merge and de-duplication stage would improve navigation
quality.

---

# 7. Overall Validation Assessment

The manual validation shows that the current prototype has **strong source
location accuracy** for the tested Persis Yu PDF.

The main remaining weaknesses are:

- Topic-label grounding
- Boundary consistency
- Overlapping and nested topic ranges
- Lack of deterministic segmentation rules

Most importantly, the previous 20/20 Location FAIL result was caused by an
inconsistent validation page-reference convention. Re-verification against
the repository's actual source PDF shows:

**Location Accuracy = 20/20 = 100%**

This should not be interpreted as evidence that every generated topic is
perfect. Location correctness and topic/segmentation quality are separate
dimensions.

---

# 8. Limitations

1. The manual validation covers 20 Topic Index entries rather than every
   generated entry in the complete deposition.

2. Topic granularity is partly subjective.

3. The current parser assumes that physical PDF page numbers correspond to
   printed transcript page numbers. This is correct for the supplied Persis
   Yu PDF, but a different PDF copy with inserted or removed pages could
   require explicit page-label mapping.

4. Several topic boundaries overlap or contain shorter nested entries.

5. The current validation establishes correctness for the tested source;
   it does not guarantee identical behavior on every future deposition.

---

# 9. Recommended Improvements

### 1. Evidence-grounded labeling

Generate each topic label strictly from the final cited testimony.

### 2. Boundary post-processing

Add automatic detection of overlapping and nested citation ranges.

### 3. Merge / de-duplication

Merge short fragments into neighboring topics when there is no genuine
subject-matter change.

### 4. Deterministic segmentation

Establish a fixed granularity rule for deciding when a new topic should
be created.

### 5. Page-label validation

Validate the physical PDF page against the printed transcript page marker
instead of assuming the two will always match.

---

# 10. Conclusion

DepoIndex demonstrates a promising functional prototype for creating a
verifiable deposition Topic Index.

For the 20 manually reviewed entries, **all 20 page/line locations were
correctly mapped to the actual Persis Yu PDF**.

The primary remaining challenges are topic-label grounding, segmentation
granularity, and overlap/nesting of topic ranges.

The system is therefore suitable as a prototype, but further validation and
post-processing are recommended before unsupervised professional use.
