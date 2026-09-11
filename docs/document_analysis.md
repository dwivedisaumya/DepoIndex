# Document Analysis: Deposition of Persis Yu

**Case Caption:** Heather Turrey vs. Vervent, Inc.  
**Deponent:** Persis Yu  
**Date:** March 28, 2023  
**File Analyzed:** `data/raw/Persis_Yu_Deposition_Problem_statement.pdf` (2,421,585 bytes)  
**Total Pages:** 122 pages  
**Reporting Agency:** Veritext Legal Solutions  

---

## 1. High-Level Document Architecture

The PDF file is a 122-page official certified deposition transcript produced by Veritext Legal Solutions in *Heather Turrey v. Vervent, Inc.* Analysis reveals a structured multi-section document:

| PDF Page Range | Printed Page Label | Section Description | Content & Structural Characteristics |
|---|---|---|---|
| **Pages 1–4** | Redacted / Unnumbered | Cover, Caption, Title & Appearances | Administrative information redacted. Explicit banner: *"Substantive testimony begins on the original transcript pages."* |
| **Page 5** | Page 5 | Index of Examination & Exhibits | Lists witness Persis Yu, examining attorney Mr. Purcell (starts p. 7), and marked exhibits (Exhibits 1–8). |
| **Page 6** | Page 6 | Preliminary Colloquy & Appearances | Counsel appearances on record (Mr. Purcell for Defendants, Mr. Blood for Plaintiff) starting on Line 22. |
| **Pages 7–88** | Pages 7–88 | **Substantive Deposition Testimony** | **Core subject matter for DepoIndex.** Direct examination of Persis Yu by Mr. John Purcell. 25 numbered lines per page. |
| **Page 89** | Page 89 | Witness Declaration / Signature Page | Declaration under penalty of perjury for Persis Yu to review and execute errata. |
| **Page 90** | Page 90 | Reporter Certification | Certificate of Certified Shorthand Reporter (CSR No. 13558) dated April 11, 2023. |
| **Pages 91–93** | Pages 91–93 | Veritext Handling & Errata Sheet | CA State Code review instructions, locked PDF notice, blank Errata Sheet. |
| **Pages 94–120** | Concordance Pages 1–27 | Word Concordance / Alphabetical Index | Court reporter index referencing words to `page:line` coordinates across the testimony. |
| **Pages 121–122** | Unnumbered | Veritext Company Certificate | Verification statement and transcript completion seal. |

---

## 2. Page & Line Numbering Mechanics

### A. PDF Page Index vs. Printed Deposition Page Number
- For the substantive testimony (**Pages 7 through 88**), the **PDF page index matches the printed deposition page label exactly (1:1 correspondence)**.
  - PDF Page 7 is Printed Page 7.
  - PDF Page 11 is Printed Page 11.
  - PDF Page 88 is Printed Page 88.
- For the post-testimony Word Index (Pages 94–120), the court reporter restarted numbering at `Page 1` through `Page 27`.
- **Engineering Decision:** To prevent any ambiguity between document index and testimony citation, every transcript line is anchored to the **printed deposition page number** as the primary legal citation coordinate, while preserving the physical `pdf_page` in metadata for viewer synchronization.

### B. Line Grid Structure
- Every deposition page adheres to the standard California 25-line legal court reporting format.
- In PyMuPDF extraction, each line is rendered as a distinct text block with its line number (1 to 25) at the left margin, followed by the transcript text, and terminated by a video timestamp on the right margin (e.g., `01:20`).
- Across all 82 testimony pages (Pages 7–88), there are exactly:
  - **2,050 total line positions** (82 pages × 25 lines = 2,050 slots).
  - **2,032 non-empty lines** containing substantive speech, attorney colloquy, speaker introductions, or formal stipulations.
  - **18 empty/blank line slots** (e.g., lines 1–10 on Page 7 before the examination commences; lines 21–25 on Page 88 after the deposition concluded at 3:42 PM).

---

## 3. Typographical & Speaker Conventions

1. **Speaker Identification:**
   - Primary examining attorney: `BY MR. PURCELL:` (line 11 on Page 7; re-announced after breaks).
   - Questions: Indented prefix `Q` (e.g., `Q You are an attorney; correct?`).
   - Witness answers: Indented prefix `A` (e.g., `A That is correct.`) or `THE WITNESS:`.
   - Objections & Colloquy: `MR. BLOOD: Same objection.`, `MR. PURCELL: Okay.`, `THE VIDEOGRAPHER: We are going off the record...`.
   - Parenthetical proceedings: `(Exhibit 1 was marked for identification.)`, `(Whereupon, the deposition concluded at 3:42 P.M.)`.

2. **Timestamps:**
   - Every substantive speech line terminates with a real-time timestamp (e.g., `01:17`, `02:45`, `03:42`).
   - Timestamps provide an orthogonal verification mechanism for chronological continuity and break detection.

3. **Exhibits Referenced:**
   - Exhibit 1: Curriculum Vitae (CV) of Persis Yu (introduced Page 10, Line 23).
   - Additional exhibits marked throughout testimony regarding student loan servicing, policy documents, and data disclosures.

---

## 4. Extraction Strategy & Canonical Representation

### A. Provenance Strategy: Source Addressability
To fulfill the requirement that **"the LLM must NEVER be trusted to invent page/line references"**, we establish an immutable source coordinate system:
- **Canonical Source ID Format:** `p{page}_l{line:02d}` (e.g., `p07_l11`, `p11_l04`, `p88_l17`).
- Each canonical line object contains:
  ```json
  {
    "source_id": "p11_l02",
    "page": 11,
    "line": 2,
    "speaker": "Q",
    "text": "You are an attorney; correct?",
    "raw_text": "      Q    You are an attorney; correct?                       01:20",
    "timestamp": "01:20",
    "is_question": true,
    "is_answer": false
  }
  ```
- **Immutable Store:** Extracted lines are compiled into `data/processed/processed_transcript.json`. Once generated, this JSON file serves as the ground truth against which all candidate proposals and evidence spans are validated.

### B. Handling Edge Cases in Text Extraction
1. **Empty Lines:** Pages 7 and 88 contain unused line slots. The parser identifies empty lines, stores them as whitespace/null with their valid coordinate, and flags them so they cannot be selected as evidence boundaries.
2. **Right-Margin Timestamps:** Timestamps must be isolated from the substantive testimony text so that semantic embeddings and topic detection focus purely on testimony content.
3. **Multi-line Sentences:** Answers and questions frequently span 2–5 lines. The canonical parser preserves individual line units while providing windowing and sentence reconstruction services for the topic detector.

---

## 5. Summary of Known Limitations

- Administrative pages (1–4) are redacted in the source file; testimony begins at Page 7 Line 11.
- Errata sheet (Page 93) is blank as this is the raw unamended deposition transcript.
- Word index (Pages 94–120) is court reporter metadata and should not be treated as witness testimony.
- Background background noises or unrecorded off-the-record breaks are indicated by parentheticals (`(Recess taken.)`) without explicit transcript lines.
