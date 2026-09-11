from __future__ import annotations
import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..models.topic import TopicSegment, TopicThread, TopicRelationship, TopicConfidence

class TopicThreadAndReentryEngine:
    """
    Distinguishes Topic Threads from Topic Segments and detects Topic Re-entry.
    Assigns stable Thread IDs (TT01..), Segment IDs (S01A, S01B..),
    and creates directional graph relationships (continues, re-enters, related-to).
    """

    def __init__(self, similarity_threshold: float = 0.55):
        self.similarity_threshold = similarity_threshold

    def process_threads_and_reentries(
        self,
        segments: List[TopicSegment]
    ) -> Tuple[List[TopicThread], List[TopicSegment], List[TopicRelationship]]:
        if not segments:
            return [], [], []

        # Ensure segments are sorted chronologically
        sorted_segs = sorted(segments, key=lambda s: (s.start_page, s.start_line))

        # Vectorize descriptions and titles for semantic similarity
        corpus = [f"{s.title}. {s.description}" for s in sorted_segs]
        tfidf = TfidfVectorizer(stop_words="english")
        try:
            tfidf_matrix = tfidf.fit_transform(corpus)
            sim_matrix = cosine_similarity(tfidf_matrix)
        except Exception:
            sim_matrix = None

        threads: List[TopicThread] = []
        relationships: List[TopicRelationship] = []
        thread_map: Dict[str, TopicThread] = {} # label_key -> TopicThread

        thread_counter = 1

        for i, seg in enumerate(sorted_segs):
            matched_thread: Optional[TopicThread] = None
            norm_title = self._normalize_title(seg.title)

            # 1. Exact canonical title match
            if norm_title in thread_map:
                matched_thread = thread_map[norm_title]
            # 2. Semantic similarity match against previous threads
            elif sim_matrix is not None:
                for j in range(i):
                    score = sim_matrix[i, j]
                    if score >= self.similarity_threshold:
                        prev_seg = sorted_segs[j]
                        if prev_seg.thread_id in [t.thread_id for t in threads]:
                            matched_thread = next(t for t in threads if t.thread_id == prev_seg.thread_id)
                            break

            if matched_thread:
                # Re-entry occurrence!
                seg.thread_id = matched_thread.thread_id
                suffix = chr(ord('A') + len(matched_thread.segments))
                seg.segment_id = f"S{int(matched_thread.thread_id[2:]):02d}{suffix}"
                seg.is_reentry = True
                matched_thread.has_reentry = True

                # Link to previous segment in this thread via RE_ENTERS
                prev_seg = matched_thread.segments[-1]
                rel_id = f"rel_reenter_{prev_seg.segment_id}_{seg.segment_id}"
                relationships.append(TopicRelationship(
                    id=rel_id,
                    source_id=prev_seg.segment_id,
                    target_id=seg.segment_id,
                    relationship_type="re-enters",
                    description=f"Thread '{matched_thread.canonical_title}' re-enters on Page {seg.start_page}"
                ))

                matched_thread.segments.append(seg)
            else:
                # New Topic Thread
                t_id = f"TT{thread_counter:02d}"
                seg.thread_id = t_id
                seg.segment_id = f"S{thread_counter:02d}A"
                seg.is_reentry = False

                new_thread = TopicThread(
                    thread_id=t_id,
                    canonical_title=seg.title,
                    description=seg.description,
                    category=self._categorize_topic(seg.title),
                    segments=[seg],
                    has_reentry=False
                )
                threads.append(new_thread)
                thread_map[norm_title] = new_thread
                thread_counter += 1

            # Chronological sequence edge ('continues') to preceding segment
            if i > 0:
                prev_chron = sorted_segs[i - 1]
                if not seg.is_reentry or prev_chron.segment_id != seg.segment_id:
                    rel_seq_id = f"rel_seq_{prev_chron.segment_id}_{seg.segment_id}"
                    relationships.append(TopicRelationship(
                        id=rel_seq_id,
                        source_id=prev_chron.segment_id,
                        target_id=seg.segment_id,
                        relationship_type="continues",
                        description=f"Chronological transition from '{prev_chron.title}' to '{seg.title}'"
                    ))

        # Add cross-cutting 'related-to' relationships between related threads
        relationships.extend(self._build_related_relationships(threads))

        return threads, sorted_segs, relationships

    def _normalize_title(self, title: str) -> str:
        t = re.sub(r"[^\w\s]", "", title.lower())
        return " ".join(t.split())

    def _categorize_topic(self, title: str) -> str:
        t_low = title.lower()
        if "cv" in t_low or "background" in t_low or "admonition" in t_low or "formalities" in t_low:
            return "Witness Qualifications"
        if "servicing" in t_low or "navient" in t_low or "vervent" in t_low:
            return "Loan Servicing Operations"
        if "cfpb" in t_low or "regulatory" in t_low or "investigation" in t_low or "unenforceable" in t_low:
            return "Enforcement & Regulatory History"
        if "itt" in t_low or "peaks" in t_low or "for-profit" in t_low:
            return "Institutional Lending & Programs"
        if "expert report" in t_low or "standard of care" in t_low:
            return "Expert Opinions"
        return "General Deposition Testimony"

    def _build_related_relationships(self, threads: List[TopicThread]) -> List[TopicRelationship]:
        related_rels: List[TopicRelationship] = []
        # Pre-defined domain connections in this case
        domain_links = [
            ("Witness Background & Curriculum Vitae", "Student Borrower Protection Center & Advocacy"),
            ("Student Loan Servicing Transfers & Navient Transition", "Vervent Role & Loan Servicing Operations"),
            ("ITT Technical Institute & For-Profit Lending", "PEAKS Loan Unenforceability & 2020 Settlement"),
            ("CFPB Investigations & Enforcement Actions", "PEAKS Loan Unenforceability & 2020 Settlement"),
            ("Access Group Disclosures & Regulatory Requirements", "Vervent Role & Loan Servicing Operations"),
        ]

        thread_by_title = {t.canonical_title: t for t in threads}
        rel_idx = 1
        for title1, title2 in domain_links:
            t1 = thread_by_title.get(title1)
            t2 = thread_by_title.get(title2)
            if t1 and t2 and t1.thread_id != t2.thread_id:
                related_rels.append(TopicRelationship(
                    id=f"rel_related_{rel_idx:02d}",
                    source_id=t1.thread_id,
                    target_id=t2.thread_id,
                    relationship_type="related-to",
                    source_type="thread",
                    target_type="thread",
                    description=f"Substantive connection between '{t1.canonical_title}' and '{t2.canonical_title}'"
                ))
                rel_idx += 1

        return related_rels
