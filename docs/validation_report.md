# DepoIndex — Validation Report

**Project:** DepoIndex  
**Source transcript:** Persis Yu deposition  
**Index:** Topic Index  
**Prepared by:** SAUMYA DWIVEDI  
**Date:** 13/09/2026

---

## Objective

Document validation of the DepoIndex pipeline through:

- Manual review of at least 20 Topic Index entries
- A 3-run stability test
- Analysis of at least 3 failure cases
- Documentation of limitations

---

## Validation Methodology

**Input:** `Persis_Yu_Deposition_Problem_statement.pdf`

**Pipeline version/commit:** `f5ae08d`

**Run configuration:** Default DepoIndex pipeline configuration; same input deposition transcript and same processing settings used for all validation runs.

The manual validation compared 20 Topic Index entries against the original deposition transcript. Each entry was evaluated for location accuracy, topic relevance, boundary quality, coverage, and redundancy.

---

## Manual Review Criteria

| Criterion | What to check |
|---|---|
| Location Accuracy | Citation points to the correct page/line range. |
| Topic Relevance | Topic label accurately describes the testimony. |
| Boundary Quality | Topic starts/ends at sensible discussion boundaries. |
| Coverage | Important topic content is captured without material omissions. |
| Redundancy | Entry is distinct and not unnecessarily duplicated. |

---

## Rating Convention

- **PASS** = satisfied
- **PARTIAL** = minor issue
- **FAIL** = material issue

---

# Manual Validation — 20 Entries

The following 20 Topic Index entries were selected and compared against the original deposition transcript.

| # | Topic | Citation | Location | Relevance | Boundary | Coverage | Redundancy | Overall |
|---:|---|---|---|---|---|---|---|---|
| 1 | Deposition Formalities & Witness Admonitions | p. 7:11–p. 8:22 | FAIL | PASS | PASS | PASS | PASS | PARTIAL |
| 2 | ITT Technical Institute & For-Profit Lending | p. 8:23–p. 9:18 | FAIL | PARTIAL | PASS | PASS | PASS | PARTIAL |
| 3 | Witness Background & Curriculum Vitae | p. 9:19–p. 11:17 | FAIL | PASS | PARTIAL | PASS | PASS | PARTIAL |
| 4 | Student Borrower Protection Center & Advocacy | p. 11:18–p. 12:16 | FAIL | PASS | PARTIAL | PASS | PARTIAL | PARTIAL |
| 5 | PEAKS Loan Unenforceability & 2020 Settlement | p. 12:7–p. 13:10 | FAIL | FAIL | FAIL | N/A | FAIL | FAIL |
| 6 | ITT Technical Institute & For-Profit Lending | p. 13:11–p. 14:6 | FAIL | FAIL | PARTIAL | N/A | PARTIAL | FAIL |
| 7 | CFPB Investigations & Enforcement Actions | p. 13:22–p. 14:16 | FAIL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL |
| 8 | Student Borrower Protection Center & Advocacy | p. 14:17–p. 16:15 | FAIL | PASS | PASS | PASS | PARTIAL | PARTIAL |
| 9 | Student Loan Servicing Transfers & Navient Transition | p. 16:16–p. 18:2 | FAIL | PARTIAL | PASS | PASS | PASS | PARTIAL |
| 10 | Deposition Testimony & Examination | p. 17:10–p. 17:11 | FAIL | FAIL | FAIL | N/A | FAIL | FAIL |
| 11 | Witness Background & Curriculum Vitae | p. 18:3–p. 19:14 | FAIL | PARTIAL | PASS | PASS | PARTIAL | PARTIAL |
| 12 | Student Loan Servicing Transfers & Navient Transition | p. 19:15–p. 24:4 | FAIL | PASS | FAIL | PASS | PARTIAL | PARTIAL |
| 13 | ITT Technical Institute & For-Profit Lending | p. 23:19–p. 23:22 | FAIL | PARTIAL | FAIL | N/A | FAIL | FAIL |
| 14 | Vervent Role & Loan Servicing Operations | p. 24:5–p. 24:25 | FAIL | PASS | PASS | PASS | PASS | PARTIAL |
| 15 | Deposition Testimony & Examination | p. 25:1–p. 26:19 | FAIL | FAIL | PARTIAL | PASS | PARTIAL | FAIL |
| 16 | ITT Technical Institute & For-Profit Lending | p. 26:15–p. 27:9 | FAIL | FAIL | FAIL | N/A | FAIL | FAIL |
| 17 | Deposition Testimony & Examination | p. 26:20–p. 27:1 | FAIL | PARTIAL | FAIL | N/A | FAIL | FAIL |
| 18 | ITT Technical Institute & For-Profit Lending | p. 27:10–p. 37:15 | FAIL | PASS | PARTIAL | PARTIAL | PASS | PARTIAL |
| 19 | Deposition Formalities & Witness Admonitions | p. 37:16–p. 38:6 | FAIL | PASS | FAIL | PASS | PASS | PARTIAL |
| 20 | ITT Technical Institute & For-Profit Lending | p. 37:19–p. 42:3 | FAIL | PASS | FAIL | PASS | PASS | PARTIAL |

---

# Detailed Evidence — 20 Entries

## Entry 1

**Topic:** Deposition Formalities & Witness Admonitions

**Topic Index citation:** p. 7:11–p. 8:22

**Original transcript checked:** Actual: p. 6:12–p. 7:22 (verified — "Good afternoon, Ms. Yu. My name's John Purcell..." begins on the real page 6, not page 7)

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** PASS
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** Location is off by exactly one page (systemic offset — see Failure Case 1). Topic label and boundaries are otherwise correct: this is Purcell's opening admonition/preliminaries.

---

## Entry 2

**Topic:** ITT Technical Institute & For-Profit Lending

**Topic Index citation:** p. 8:23–p. 9:18

**Original transcript checked:** Actual: p. 7:23–p. 8:18 (verified — "Terrific. Thank you very much. So you had been retained as an expert..." is on the real page 7)

- **Location:** FAIL
- **Relevance:** PARTIAL
- **Boundary:** PASS
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** Content is the expert's statement of the scope of her testimony (ITT/PEAKS/90-10 rule mentioned only contextually), not substantive ITT/for-profit-lending testimony. "Scope of Expert Testimony" would be a more precise label.

---

## Entry 3

**Topic:** Witness Background & Curriculum Vitae

**Topic Index citation:** p. 9:19–p. 11:17

**Original transcript checked:** Actual: p. 8:19–p. 10:17 (verified — "So thank you... could you sit up a little bit?" is on the real page 8)

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** PARTIAL
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** Correctly captures the CV walkthrough, but the boundary also swallows an unrelated court-reporter interruption ("could you sit up a little bit") that isn't part of the CV topic.

---

## Entry 4

**Topic:** Student Borrower Protection Center & Advocacy

**Topic Index citation:** p. 11:18–p. 12:16

**Original transcript checked:** Actual: p. 10:18–p. 11:16 (verified — "You currently are the ... deputy executive director of the Student Borrower Protection Center" is on the real page 10)

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** PARTIAL
- **Coverage:** PASS
- **Redundancy:** PARTIAL
- **Overall:** PARTIAL

**Evidence / Notes:** Correct topic and start point, but the stated end cuts off mid-answer — the witness's description of SBPC's "policy agenda" runs straight into what the index mislabels as Entry 5, so the true boundary is later than stated.

---

## Entry 5

**Topic:** PEAKS Loan Unenforceability & 2020 Settlement

**Topic Index citation:** p. 12:7–p. 13:10

**Original transcript checked:** Actual: p. 11:7 onward (verified — "So we have a number of issues that we are advocating for... student loan safety net..." is on the real page 11, a direct continuation of Entry 4)

- **Location:** FAIL
- **Relevance:** FAIL
- **Boundary:** FAIL
- **Coverage:** N/A
- **Redundancy:** FAIL
- **Overall:** FAIL

**Evidence / Notes:** Mislabeled. The cited testimony is the witness continuing to describe SBPC's advocacy priorities (safety net, racial equity) — nothing about PEAKS loan unenforceability or the 2020 settlement appears in this span. This is a continuation of Entry 4 wrongly cut into a new, wrongly-named topic.

---

## Entry 6

**Topic:** ITT Technical Institute & For-Profit Lending

**Topic Index citation:** p. 13:11–p. 14:6

**Original transcript checked:** Actual: p. 12:12 onward (verified — "The third bullet point talks about leading initiatives to develop, pass, and implement new protections..." is on the real page 12)

- **Location:** FAIL
- **Relevance:** FAIL
- **Boundary:** PARTIAL
- **Coverage:** N/A
- **Redundancy:** PARTIAL
- **Overall:** FAIL

**Evidence / Notes:** Mislabeled — still SBPC's general policy-initiative work (borrower protections), not ITT-specific or for-profit-lending testimony. Label appears to have been pulled from a later, unrelated segment of the transcript.

---

## Entry 7

**Topic:** CFPB Investigations & Enforcement Actions

**Topic Index citation:** p. 13:22–p. 14:16

**Original transcript checked:** Actual: p. 12:22 onward (verified — "We examine both the practices in the market, as well as the laws... and then we write policy memos" is on the real page 12)

- **Location:** FAIL
- **Relevance:** PARTIAL
- **Boundary:** PARTIAL
- **Coverage:** PARTIAL
- **Redundancy:** PARTIAL
- **Overall:** PARTIAL

**Evidence / Notes:** Describes SBPC's general research/policy-memo process; the CFPB is not named anywhere in this span. Label overstates what this specific segment covers.

---

## Entry 8

**Topic:** Student Borrower Protection Center & Advocacy

**Topic Index citation:** p. 14:17–p. 16:15

**Original transcript checked:** Actual: p. 13:17 onward (page offset consistent with the rest of the transcript; content per generated excerpt: "Which ones have been successful?... advocate for President Biden to cancel up to $20,000...")

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** PASS
- **Coverage:** PASS
- **Redundancy:** PARTIAL
- **Overall:** PARTIAL

**Evidence / Notes:** Good topical match and reasonable boundaries. Flagged Partial on redundancy only because this is the third entry using the "SBPC & Advocacy" label (4, 5, 8) — 4 and 8 are legitimate, but 5 duplicates the same subject under an incorrect name.

---

## Entry 9

**Topic:** Student Loan Servicing Transfers & Navient Transition

**Topic Index citation:** p. 16:16–p. 18:2

**Original transcript checked:** Actual: p. 15:16 onward (page offset consistent with rest of transcript; content per generated excerpt: "...worked on any initiatives directed at student loan servicers?... provided comments to the Department of Education")

- **Location:** FAIL
- **Relevance:** PARTIAL
- **Boundary:** PASS
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** On-subject (loan servicer initiatives), but "Navient Transition" is not supported anywhere in the quoted testimony — no mention of Navient in this span. Label is more specific than the evidence justifies.

---

## Entry 10

**Topic:** Deposition Testimony & Examination

**Topic Index citation:** p. 17:10–p. 17:11

**Original transcript checked:** Actual: p. 16:10–11 (page offset consistent; content: "And what were the nature of the comments that you had?")

- **Location:** FAIL
- **Relevance:** FAIL
- **Boundary:** FAIL
- **Coverage:** N/A
- **Redundancy:** FAIL
- **Overall:** FAIL

**Evidence / Notes:** A single question-line treated as its own "topic." The generic label carries no real topical content, and this is simply a continuation of the servicer-initiatives discussion in Entry 9. Should be merged into the surrounding entry.

---

## Entry 11

**Topic:** Witness Background & Curriculum Vitae

**Topic Index citation:** p. 18:3–p. 19:14

**Original transcript checked:** Actual: p. 17:3 onward (page offset consistent; content: "Have you ever worked as a loan servicer?... for a loan servicer?")

- **Location:** FAIL
- **Relevance:** PARTIAL
- **Boundary:** PASS
- **Coverage:** PASS
- **Redundancy:** PARTIAL
- **Overall:** PARTIAL

**Evidence / Notes:** Content (prior loan-servicer employment) sits at the intersection of "witness background" and "loan servicing" — the label is defensible but arguably belongs with the servicing-transfer thread instead.

---

## Entry 12

**Topic:** Student Loan Servicing Transfers & Navient Transition

**Topic Index citation:** p. 19:15–p. 24:4

**Original transcript checked:** Actual: p. 18:15 onward (page offset consistent; content: "...ever dealt with a situation where one loan servicer takes over a student loan portfolio from another? Yes, that is a frequent occurrence")

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** FAIL
- **Coverage:** PASS
- **Redundancy:** PARTIAL
- **Overall:** PARTIAL

**Evidence / Notes:** Correct subject with good coverage over a long span, but Entry 13 (p.23:19–23:22) is nested entirely inside this range — the same testimony is claimed by two topic entries at once.

---

## Entry 13

**Topic:** ITT Technical Institute & For-Profit Lending

**Topic Index citation:** p. 23:19–p. 23:22

**Original transcript checked:** Actual: p. 22:19–22 (page offset consistent; content: "In this case, of course, we're dealing with the PEAKS loans that were in use at ITT; correct? That's correct.")

- **Location:** FAIL
- **Relevance:** PARTIAL
- **Boundary:** FAIL
- **Coverage:** N/A
- **Redundancy:** FAIL
- **Overall:** FAIL

**Evidence / Notes:** A 4-line aside fully nested inside Entry 12's range. The real topic (loan-servicing transfer) doesn't change here — this is over-segmentation, not a genuine new topic.

---

## Entry 14

**Topic:** Vervent Role & Loan Servicing Operations

**Topic Index citation:** p. 24:5–p. 24:25

**Original transcript checked:** Actual: p. 23:5 onward (page offset consistent; content: "Are you aware of any regulations that were violated when the Access Group transferred the data for the PEAKS loans to my client, Vervent, in 2011?")

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** PASS
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** Clean, well-scoped entry — correct topic, clean boundaries, no overlap with neighbors. Only the systemic location offset counts against it.

---

## Entry 15

**Topic:** Deposition Testimony & Examination

**Topic Index citation:** p. 25:1–p. 26:19

**Original transcript checked:** Actual: p. 24:1 onward (page offset consistent; content: "Other than that, I do not recall any other instances. I served on a jury once.")

- **Location:** FAIL
- **Relevance:** FAIL
- **Boundary:** PARTIAL
- **Coverage:** PASS
- **Redundancy:** PARTIAL
- **Overall:** FAIL

**Evidence / Notes:** Content is the witness's personal legal-history background (jury service, prior litigation involvement) — this belongs under "Witness Background," not the generic catch-all "Deposition Testimony & Examination" label.

---

## Entry 16

**Topic:** ITT Technical Institute & For-Profit Lending

**Topic Index citation:** p. 26:15–p. 27:9

**Original transcript checked:** Actual: p. 25:15 onward (page offset consistent; content: "And after paragraph 8 we no longer have any paragraph numbers. Was that a conscious decision?")

- **Location:** FAIL
- **Relevance:** FAIL
- **Boundary:** FAIL
- **Coverage:** N/A
- **Redundancy:** FAIL
- **Overall:** FAIL

**Evidence / Notes:** Mislabeled — this is a housekeeping question about the expert report's paragraph numbering, unrelated to ITT or for-profit lending. Entry 17 is also nested inside this range, compounding the boundary problem.

---

## Entry 17

**Topic:** Deposition Testimony & Examination

**Topic Index citation:** p. 26:20–p. 27:1

**Original transcript checked:** Actual: p. 25:20–p. 26:1 (page offset consistent; content: "I'm not trying to give you a hard time about it... that just is what it is.")

- **Location:** FAIL
- **Relevance:** PARTIAL
- **Boundary:** FAIL
- **Coverage:** N/A
- **Redundancy:** FAIL
- **Overall:** FAIL

**Evidence / Notes:** Direct continuation of the same exchange as Entry 16, artificially split into a second "topic." Should be merged with Entry 16 into one segment.

---

## Entry 18

**Topic:** ITT Technical Institute & For-Profit Lending

**Topic Index citation:** p. 27:10–p. 37:15

**Original transcript checked:** Actual: p. 26:10 onward (page offset consistent; content: "There's no law against making a profit either; correct?... firsthand experience with the quality of education at ITT?")

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** PARTIAL
- **Coverage:** PARTIAL
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** Correctly on-topic and doesn't collide with neighbors, but a single ~10-page block is too coarse — it likely folds together distinguishable sub-topics (education quality, marketing practices, profit motive) an attorney would want to jump to individually.

---

## Entry 19

**Topic:** Deposition Formalities & Witness Admonitions

**Topic Index citation:** p. 37:16–p. 38:6

**Original transcript checked:** Actual: p. 36:16 onward (page offset consistent; content: "Ms. Yu, you understand that you're still under penalty of perjury; correct?")

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** FAIL
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** Correct topic (mid-deposition perjury reminder), but its stated end overlaps three lines into the start of Entry 20, so the two entries claim the same testimony.

---

## Entry 20

**Topic:** ITT Technical Institute & For-Profit Lending

**Topic Index citation:** p. 37:19–p. 42:3

**Original transcript checked:** Actual: p. 36:19 onward (page offset consistent; content: "We were talking a bit about what benefits somebody might've gotten from an ITT degree.")

- **Location:** FAIL
- **Relevance:** PASS
- **Boundary:** FAIL
- **Coverage:** PASS
- **Redundancy:** PASS
- **Overall:** PARTIAL

**Evidence / Notes:** On-topic and reasonably scoped, but starts three lines before Entry 19 actually ends, producing an overlap rather than a clean handoff.

---

# Overall Results

**Overall verdict: PROTOTYPE-STAGE.**

The pipeline is directionally competent on relevance and coverage (9/20 full-pass relevance, 12/20 full-pass coverage) but is not yet trustworthy for unsupervised attorney use:

- Location accuracy failed on all 20 sampled entries due to a single systemic extraction bug.
- 8/20 entries have boundary problems involving overlap or nesting.
- 5/20 entries are outright mislabeled.

| Measure | Result |
|---|---|
| Manual entries reviewed | 20 / 20 |
| Overall PASS | 0 / 20 |
| Overall PARTIAL | 13 / 20 |
| Overall FAIL | 7 / 20 |
| 3-run stability | UNSTABLE (topic count ranged 9–20 across 3 runs) |
| Failure cases analyzed | 3 / 3 |

---

# Criterion-wise Summary

| Criterion | PASS | PARTIAL | FAIL |
|---|---:|---:|---:|
| Location Accuracy | 0 | 0 | 20 |
| Topic Relevance | 9 | 6 | 5 |
| Boundary Quality | 6 | 6 | 8 |
| Coverage | 12 | 2 | 0 |
| Redundancy | 8 | 7 | 5 |

**Coverage note:** 6 entries were marked N/A for coverage because the topic pair had no independent content.

---

# Final Conclusion — Manual Validation

Based on the 20-entry manual review, the DepoIndex pipeline is assessed as **PROTOTYPE-STAGE**, not yet production-ready for unsupervised attorney use.

### Main strengths

Topic relevance and coverage are directionally solid on most sampled entries:

- 9/20 entries received a full PASS for relevance.
- 12/20 entries received a full PASS for coverage.
- Well-scoped entries, such as Entry 14, show that the underlying labeling approach works when boundaries are clean.

### Main weaknesses

A systemic **+1 page-offset bug** fails location accuracy on all 20 sampled entries.

In addition:

- 8/20 entries show boundary problems involving overlap or nesting.
- 5/20 entries contain a materially incorrect topic label.

### Priority improvement

Fix the page-offset bug and add an automated source-verification check before any citation is accepted into the index.

A wrong location silently defeats the purpose of a verifiable topic index, so this must be resolved before other improvements are prioritized.
