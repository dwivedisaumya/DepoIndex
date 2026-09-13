# DepoIndex — Stability Report

**Project:** DepoIndex  
**Source transcript:** Persis Yu deposition  
**Index:** Topic Index  
**Prepared by:** SAUMYA DWIVEDI  
**Date:** 13/09/2026

---

# 1. Stability Test

The intended test was to run the same pipeline on the same input and
configuration three times and compare the outputs.

An important limitation applies:

> The underlying automated pipeline was not available to re-execute in the
> validation environment. Therefore, Run 2 and Run 3 are manual proxy runs,
> not genuine automated pipeline executions.

The proxy runs were used as an honest substitute for assessing segmentation
variance.

---

# 2. Run Configuration

| Item | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Run description | Supplied `topic_index.md` | Independent manual re-segmentation | Independent manual re-segmentation |
| Input | Persis Yu deposition, real pages 6–42 | Same range | Same range |
| Method | Pre-generated system output | Manual transcript re-read | Manual transcript re-read |
| Granularity | Generated system output | Moderate | Coarser |
| Topic count | 20 raw entries | 15 topics | 9 topics |

Run 1 represents the supplied generated Topic Index.

Run 2 and Run 3 were independently created from the raw transcript text
without referring to the earlier segmentation.

---

# 3. Topic Count Consistency

## Result: UNSTABLE

Observed counts:

- Run 1: **20 raw entries**
- Run 2: **15 topics**
- Run 3: **9 topics**

The observed range is therefore **9–20 topics**.

This demonstrates substantial sensitivity to segmentation granularity.

However, because Run 2 and Run 3 were manual proxy runs with intentionally
different granularity, these numbers should not be treated as controlled
automated-run statistics.

---

# 4. Topic Title Consistency

## Result: MOSTLY STABLE AT THE THEME LEVEL

All runs identified broad themes such as:

- Deposition formalities
- Witness background / CV
- SBPC advocacy
- Student loan servicing and transfers
- PEAKS / Vervent-related testimony
- ITT Technical Institute / for-profit lending

Exact labels differed depending on segmentation granularity.

Therefore, broad subject recognition appears more stable than exact topic
naming.

---

# 5. Citation / Location Consistency

The location re-check against the actual Persis Yu PDF showed that the
generated Run 1 citations map correctly to the physical and printed page
numbers.

The 20 sampled locations were verified as:

**20 PASS / 0 PARTIAL / 0 FAIL**

The stability test itself does not establish that repeated automated
executions would always produce identical citation boundaries because the
actual pipeline could not be re-executed three times.

---

# 6. Boundary Consistency

## Result: UNSTABLE

The main source of variance was merge/split behavior.

For example:

- A long discussion can be represented as one broad topic.
- The same discussion can be split into several smaller topics.
- Short questions or asides can become independent entries.
- Related testimony can be merged into a neighboring topic.

The loan-servicing discussion around real pages 15–22 showed substantial
differences in segmentation granularity.

---

# 7. Stable Segment

The short, self-contained PEAKS-to-Vervent Q&A around real p. 22:20–23:13
remained comparatively stable across the reviewed segmentations.

This suggests that short, clearly bounded exchanges are easier to segment
consistently than long discursive answers.

---

# 8. Overall Stability Verdict

**UNSTABLE AS CURRENTLY SPECIFIED**

The observed topic count varied substantially across the three observed
segmentations.

The main weakness is segmentation granularity rather than source-page
addressability.

---

# 9. Limitations

1. Run 1 was a supplied pre-generated output.

2. Run 2 and Run 3 were manual proxy re-segmentations rather than genuine
   automated executions.

3. The proxy runs intentionally used different segmentation granularity.

4. Therefore, the observed topic-count range demonstrates sensitivity to
   segmentation choices but is not a controlled automated stability metric.

5. The stability test covered the same approximately 37-page window used
   for the reviewed entries rather than the entire deposition.

---

# 10. Corrective Actions

A future controlled stability test should:

1. Execute the actual pipeline three or more times.

2. Use temperature 0 and deterministic chunking.

3. Log topic count, labels, boundaries, and citations for every run.

4. Compare topic overlap and boundary agreement across runs.

5. Add a merge / de-duplication stage.

6. Establish a fixed topic-granularity rule.

7. Add automated provenance validation for every generated citation.

---

# Conclusion

The prototype consistently identifies broad subject areas, but segmentation
granularity remains sensitive to how testimony is divided into topics.

A controlled automated re-run is required before claiming a formal automated
stability metric.
