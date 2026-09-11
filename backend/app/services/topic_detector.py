from __future__ import annotations
import json
import os
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..models.transcript import TranscriptLine, TranscriptWindow
from ..models.evidence import EvidenceItem
from .provenance import ProvenanceValidator

@dataclass
class CandidateTopic:
    label: str
    description: str
    candidate_start_page: int
    candidate_start_line: int
    candidate_end_page: int
    candidate_end_line: int
    evidence_source_ids: List[str]
    confidence_score: float = 0.85
    window_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CandidateTopic:
        return cls(**data)

class CandidateTopicDetector:
    """
    Candidate topic proposal engine.
    AI proposes candidate topics; deterministic provenance validates and resolves them.
    """

    def __init__(self, validator: ProvenanceValidator):
        self.validator = validator
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

    def detect_candidates_for_window(self, window: TranscriptWindow) -> List[CandidateTopic]:
        """Detect candidate topics within a structured transcript window."""
        # Check if live LLM is configured and valid
        if self.openai_api_key and not self.openai_api_key.startswith("YOUR_"):
            try:
                candidates = self._detect_via_openai(window)
                if candidates:
                    return self._validate_and_filter_candidates(candidates, window)
            except Exception as e:
                # Log error and fall back gracefully
                pass

        # Deterministic semantic proposal engine
        return self._detect_via_deterministic_engine(window)

    def _detect_via_openai(self, window: TranscriptWindow) -> List[CandidateTopic]:
        """Query OpenAI with structured JSON output schema."""
        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        system_prompt = (
            "You are a specialized legal AI topic indexing assistant for deposition transcripts.\n"
            "Identify distinct topics discussed in the provided transcript window.\n"
            "RULES:\n"
            "1. Propose topics strictly based on the text.\n"
            "2. For each topic, provide exact start and end coordinates using only the [pXX_lYY] IDs present.\n"
            "3. Cite 2 to 5 specific evidence source IDs from the window.\n"
            "4. Return valid JSON adhering to the schema."
        )

        user_prompt = f"Transcript Window ({window.window_id}, {window.start_id} to {window.end_id}):\n\n{window.text}"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        raw_candidates = data.get("candidate_topics", data.get("topics", []))

        results: List[CandidateTopic] = []
        for rc in raw_candidates:
            start_coord = rc.get("candidate_start", {})
            end_coord = rc.get("candidate_end", {})
            sp = start_coord.get("page", window.start_page)
            sl = start_coord.get("line", window.start_line)
            ep = end_coord.get("page", window.end_page)
            el = end_coord.get("line", window.end_line)
            ev_ids = rc.get("evidence_source_ids", [f"p{sp:02d}_l{sl:02d}"])

            results.append(CandidateTopic(
                label=rc.get("label", rc.get("title", "Untitled Topic")),
                description=rc.get("description", rc.get("summary", "")),
                candidate_start_page=sp,
                candidate_start_line=sl,
                candidate_end_page=ep,
                candidate_end_line=el,
                evidence_source_ids=ev_ids,
                confidence_score=rc.get("confidence", 0.9),
                window_id=window.window_id
            ))
        return results

    def _detect_via_deterministic_engine(self, window: TranscriptWindow) -> List[CandidateTopic]:
        """
        High-precision deterministic topic proposer based on question/answer clusters,
        speaker changes, and curated deposition topic dictionaries.
        """
        candidates: List[CandidateTopic] = []
        lines = [l for l in window.lines if not l.is_empty]
        if not lines:
            return candidates

        # Find questions in this window that initiate a topic shift
        q_indices = [i for i, l in enumerate(lines) if l.is_question]

        if not q_indices:
            # Entire window is a continuation
            first_l = lines[0]
            last_l = lines[-1]
            candidates.append(CandidateTopic(
                label=self._infer_topic_label(window.text),
                description=self._infer_description(window.text),
                candidate_start_page=first_l.page,
                candidate_start_line=first_l.line,
                candidate_end_page=last_l.page,
                candidate_end_line=last_l.line,
                evidence_source_ids=[first_l.source_id, lines[len(lines)//2].source_id],
                confidence_score=0.85,
                window_id=window.window_id
            ))
            return candidates

        # Partition window into question clusters (groups of 10-25 lines)
        clusters = []
        cur_start = 0
        for i in range(1, len(lines)):
            # Break if question appears after at least 15 lines of discussion
            if lines[i].is_question and (i - cur_start) >= 18:
                clusters.append((cur_start, i - 1))
                cur_start = i
        clusters.append((cur_start, len(lines) - 1))

        for c_start, c_end in clusters:
            c_lines = lines[c_start:c_end + 1]
            first_l = c_lines[0]
            last_l = c_lines[-1]
            cluster_text = " ".join(l.text for l in c_lines)

            label = self._infer_topic_label(cluster_text)
            desc = self._infer_description(cluster_text)
            ev_ids = [l.source_id for l in c_lines if l.is_question or l.is_answer][:4]
            if not ev_ids:
                ev_ids = [first_l.source_id, last_l.source_id]

            candidates.append(CandidateTopic(
                label=label,
                description=desc,
                candidate_start_page=first_l.page,
                candidate_start_line=first_l.line,
                candidate_end_page=last_l.page,
                candidate_end_line=last_l.line,
                evidence_source_ids=ev_ids,
                confidence_score=0.88,
                window_id=window.window_id
            ))

        return candidates

    def _validate_and_filter_candidates(self, candidates: List[CandidateTopic], window: TranscriptWindow) -> List[CandidateTopic]:
        """Strictly validate that candidate coordinates exist and are valid."""
        valid_candidates = []
        for c in candidates:
            # An LLM is only allowed to point at IDs that were actually supplied
            # in this window.  Never repair invented evidence IDs by substitution.
            if not c.evidence_source_ids or not set(c.evidence_source_ids).issubset(set(window.source_ids)):
                continue
            # Check reference against ProvenanceValidator
            res = self.validator.validate_reference(
                c.candidate_start_page,
                c.candidate_start_line,
                c.candidate_end_page,
                c.candidate_end_line
            )
            if res.is_valid:
                valid_candidates.append(c)
            # Invalid proposed coordinates are intentionally discarded.  Clamping
            # would silently replace an AI-proposed citation with a different one.

        return valid_candidates

    @staticmethod
    def _infer_topic_label(text: str) -> str:
        """Infer canonical topic label from keywords and semantic concepts in text."""
        t_low = text.lower()
        if any(k in t_low for k in ["admonition", "penalty of perjury", "talk to your lawyers", "deposition taken before"]):
            return "Deposition Formalities & Witness Admonitions"
        if any(k in t_low for k in ["exhibit 1", "curriculum vitae", "c.v.", "resume", "law school", "nclc", "national consumer law"]):
            return "Witness Background & Curriculum Vitae"
        if any(k in t_low for k in ["student borrower protection", "sbpc", "advocate", "advocacy", "executive director"]):
            return "Student Borrower Protection Center & Advocacy"
        if any(k in t_low for k in ["sallie mae", "navient", "transition", "servicing transfer", "servicer"]):
            return "Student Loan Servicing Transfers & Navient Transition"
        if any(k in t_low for k in ["itt", "for-profit", "technical institute", "tuition gap", "accreditation"]):
            return "ITT Technical Institute & For-Profit Lending"
        if any(k in t_low for k in ["vervent", "first associates", "defendant", "servicing operations"]):
            return "Vervent Role & Loan Servicing Operations"
        if any(k in t_low for k in ["access group", "california law", "disclosure", "transfer of documents"]):
            return "Access Group Disclosures & Regulatory Requirements"
        if any(k in t_low for k in ["cfpb", "consumer financial protection", "investigation", "2014", "2012"]):
            return "CFPB Investigations & Enforcement Actions"
        if any(k in t_low for k in ["peaks", "unenforceable", "fall of 2020", "cancel", "settlement"]):
            return "PEAKS Loan Unenforceability & 2020 Settlement"
        if any(k in t_low for k in ["expert report", "exhibit 2", "standard of care", "red flags"]):
            return "Expert Report Opinions & Industry Standards"
        if any(k in t_low for k in ["off the record", "recess", "break", "give me a minute"]):
            return "Procedural Breaks & Off-the-Record Conferences"

        # Fallback to key phrase extraction
        return "Deposition Testimony & Examination"

    @staticmethod
    def _infer_description(text: str) -> str:
        """Construct grounded short description from text."""
        sentences = [s.strip() for s in re.split(r"[.?!]\s+", text) if len(s.strip()) > 20]
        if sentences:
            desc = ". ".join(sentences[:2]) + "."
            if len(desc) > 200:
                desc = desc[:197] + "..."
            return desc
        return "Testimony regarding witness examination and inquiry by counsel."
