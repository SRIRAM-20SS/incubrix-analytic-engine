"""
Provider Adapters Module
Implements collection adapters for Google Search and the four AI assistants:
ChatGPT, Google Gemini, Perplexity, and Claude.
Provides distinct mention vs citation detection and manual capture parsing.
"""

import hashlib
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

KNOWN_COMPETITORS = [
    "OpusClip", "Descript", "Kapwing", "Munch", "Klap", "Vidyo.ai",
    "Riverside.fm", "Veed.io", "Submagic", "CapCut", "InVideo",
    "Headliner", "HeyGen", "StreamLadder", "Eklipse", "Topaz Video AI",
    "Adobe Premiere Pro", "DaVinci Resolve", "Auphonic", "LALAL.AI"
]


class BaseAdapter:
    def __init__(self, provider_name: str, default_model: str):
        self.provider_name = provider_name
        self.default_model = default_model

    @staticmethod
    def detect_brand_mention(text: str, brand: str = "IncuBrix") -> bool:
        """Determines if the brand name appears in text (case-insensitive boundary match)."""
        if not text:
            return False
        pattern = rf"\b{re.escape(brand)}\b"
        return bool(re.search(pattern, text, re.IGNORECASE))

    @staticmethod
    def detect_brand_citation(citation_urls: List[str], domain: str = "incubrix.com") -> bool:
        """Determines if any citation URL points to the domain."""
        if not citation_urls:
            return False
        for url in citation_urls:
            if not isinstance(url, str):
                continue
            parsed = urlparse(url.lower().strip())
            if domain in parsed.netloc or domain in url.lower():
                return True
        return False

    @staticmethod
    def extract_competitors(text: str) -> List[str]:
        """Identifies known competitor mentions from text."""
        if not text:
            return []
        found = []
        for comp in KNOWN_COMPETITORS:
            # Match word boundary or hyphenated/dot variants
            clean_comp = re.escape(comp.replace(".fm", "").replace(".io", "").replace(".ai", ""))
            if re.search(rf"\b{clean_comp}\b", text, re.IGNORECASE):
                found.append(comp)
        return sorted(list(set(found)))

    @staticmethod
    def compute_sha256(text: str) -> str:
        """Computes deterministic SHA-256 hash for raw answer reproducibility."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()


class GoogleSearchAdapter(BaseAdapter):
    def __init__(self, default_model: str = "Desktop SERP 2026"):
        super().__init__("Google Search", default_model)

    def parse_evidence(self, question_id: str, evidence: Dict[str, Any], day_number: int) -> Dict[str, Any]:
        gs = evidence.get("google_search", {})
        meta = evidence.get("collection_metadata", {})
        ts = meta.get(f"day{day_number}_timestamp") or meta.get("day1_timestamp", "2026-10-21T10:00:00Z")

        pos = str(gs.get("position", ">100"))
        num_rank = None
        if pos.isdigit():
            num_rank = int(pos)

        ab_type = gs.get("answer_box_or_ai_overview", "None")
        paa_present = 1 if "PAA" in str(ab_type) or evidence.get("source_type") == "People Also Ask" else 0
        ai_overview_present = 1 if ab_type == "AI Overview" else 0
        snippet_present = 1 if ab_type == "Answer box" else 0

        # Raw representation
        raw_repr = (
            f"Query: {evidence.get('question')}\n"
            f"Google Position: {pos}\n"
            f"SERP Features: {ab_type}\n"
            f"Quoted URL: {gs.get('quoted_source_url')}\n"
            f"Top Domains: {', '.join(gs.get('top_ranking_domains', []))}"
        )

        return {
            "response_id": f"RESP-{question_id}-D{day_number}-GOOGLE",
            "question_id": question_id,
            "provider": self.provider_name,
            "model_version": self.default_model,
            "checked_at": ts,
            "market": evidence.get("market", "US"),
            "location_setting": meta.get("ip_location", "GeoIP: US"),
            "google_position": pos,
            "google_numeric_rank": num_rank,
            "incubrix_ranking_url": gs.get("incubrix_ranking_url"),
            "featured_snippet_present": snippet_present,
            "paa_present": paa_present,
            "ai_overview_present": ai_overview_present,
            "answer_box_type": ab_type,
            "quoted_source_url": gs.get("quoted_source_url"),
            "raw_response_text": raw_repr,
            "response_hash": self.compute_sha256(raw_repr),
            "incubrix_mentioned": 1 if self.detect_brand_mention(raw_repr) else 0,
            "incubrix_cited": 1 if self.detect_brand_citation([gs.get("quoted_source_url") or ""]) else 0,
            "collection_status": "Success",
            "error_message": None
        }


class ChatGPTAdapter(BaseAdapter):
    def __init__(self, default_model: str = "OpenAI GPT-4o (Search)"):
        super().__init__("OpenAI ChatGPT", default_model)

    def parse_evidence(self, question_id: str, evidence: Dict[str, Any], day_number: int) -> Dict[str, Any]:
        ai_sec = evidence.get("ai_assistants", {}).get("chatgpt", {})
        meta = evidence.get("collection_metadata", {})
        ts = meta.get(f"day{day_number}_timestamp") or meta.get("day1_timestamp", "2026-10-21T10:00:00Z")

        summary = ai_sec.get("response_summary", "")
        status = ai_sec.get("incubrix_status", "Not mentioned")
        comps = ai_sec.get("competitors_mentioned", [])
        engine = ai_sec.get("engine", self.default_model)

        is_mentioned = 1 if status.lower() in ("mentioned", "cited") or self.detect_brand_mention(summary) else 0
        is_cited = 1 if status.lower() == "cited" else 0

        return {
            "response_id": f"RESP-{question_id}-D{day_number}-CHATGPT",
            "question_id": question_id,
            "provider": self.provider_name,
            "model_version": engine,
            "checked_at": ts,
            "market": evidence.get("market", "US"),
            "location_setting": meta.get("ip_location", "GeoIP: US"),
            "status_declared": status,
            "competitors_mentioned": comps,
            "citation_urls": ai_sec.get("cited_urls", []),
            "raw_response_text": summary,
            "response_hash": self.compute_sha256(summary or f"{question_id}-chatgpt"),
            "incubrix_mentioned": is_mentioned,
            "incubrix_cited": is_cited,
            "collection_status": "Success" if summary else "Missing",
            "error_message": None
        }


class GeminiAdapter(BaseAdapter):
    def __init__(self, default_model: str = "Google Gemini 1.5 Pro"):
        super().__init__("Google Gemini", default_model)

    def parse_evidence(self, question_id: str, evidence: Dict[str, Any], day_number: int) -> Dict[str, Any]:
        ai_sec = evidence.get("ai_assistants", {}).get("gemini", {})
        meta = evidence.get("collection_metadata", {})
        ts = meta.get(f"day{day_number}_timestamp") or meta.get("day1_timestamp", "2026-10-21T10:00:00Z")

        summary = ai_sec.get("response_summary", "")
        status = ai_sec.get("incubrix_status", "Not mentioned")
        comps = ai_sec.get("competitors_mentioned", [])
        engine = ai_sec.get("engine", self.default_model)

        is_mentioned = 1 if status.lower() in ("mentioned", "cited") or self.detect_brand_mention(summary) else 0
        is_cited = 1 if status.lower() == "cited" else 0

        return {
            "response_id": f"RESP-{question_id}-D{day_number}-GEMINI",
            "question_id": question_id,
            "provider": self.provider_name,
            "model_version": engine,
            "checked_at": ts,
            "market": evidence.get("market", "US"),
            "location_setting": meta.get("ip_location", "GeoIP: US"),
            "status_declared": status,
            "competitors_mentioned": comps,
            "citation_urls": ai_sec.get("cited_urls", []),
            "raw_response_text": summary,
            "response_hash": self.compute_sha256(summary or f"{question_id}-gemini"),
            "incubrix_mentioned": is_mentioned,
            "incubrix_cited": is_cited,
            "collection_status": "Success" if summary else "Missing",
            "error_message": None
        }


class PerplexityAdapter(BaseAdapter):
    def __init__(self, default_model: str = "Perplexity AI (Sonar / Web)"):
        super().__init__("Perplexity AI", default_model)

    def parse_evidence(self, question_id: str, evidence: Dict[str, Any], day_number: int) -> Dict[str, Any]:
        ai_sec = evidence.get("ai_assistants", {}).get("perplexity", {})
        meta = evidence.get("collection_metadata", {})
        ts = meta.get(f"day{day_number}_timestamp") or meta.get("day1_timestamp", "2026-10-21T10:00:00Z")

        summary = ai_sec.get("response_summary", "")
        status = ai_sec.get("incubrix_status", "Not mentioned")
        comps = ai_sec.get("competitors_mentioned", [])
        citations = ai_sec.get("cited_urls", [])
        engine = ai_sec.get("engine", self.default_model)

        is_mentioned = 1 if status.lower() in ("mentioned", "cited") or self.detect_brand_mention(summary) else 0
        is_cited = 1 if self.detect_brand_citation(citations) else 0

        return {
            "response_id": f"RESP-{question_id}-D{day_number}-PERPLEXITY",
            "question_id": question_id,
            "provider": self.provider_name,
            "model_version": engine,
            "checked_at": ts,
            "market": evidence.get("market", "US"),
            "location_setting": meta.get("ip_location", "GeoIP: US"),
            "status_declared": status,
            "competitors_mentioned": comps,
            "citation_urls": citations,
            "raw_response_text": summary,
            "response_hash": self.compute_sha256(summary or f"{question_id}-perplexity"),
            "incubrix_mentioned": is_mentioned,
            "incubrix_cited": is_cited,
            "collection_status": "Success" if summary else "Missing",
            "error_message": None
        }


class ClaudeAdapter(BaseAdapter):
    def __init__(self, default_model: str = "Claude 3.5 Sonnet / MS Copilot"):
        super().__init__("Anthropic Claude", default_model)

    def parse_evidence(self, question_id: str, evidence: Dict[str, Any], day_number: int) -> Dict[str, Any]:
        ai_sec = evidence.get("ai_assistants", {}).get("claude_or_copilot", {})
        meta = evidence.get("collection_metadata", {})
        ts = meta.get(f"day{day_number}_timestamp") or meta.get("day1_timestamp", "2026-10-21T10:00:00Z")

        summary = ai_sec.get("response_summary", "")
        status = ai_sec.get("incubrix_status", "Not mentioned")
        comps = ai_sec.get("competitors_mentioned", [])
        engine = ai_sec.get("engine", self.default_model)

        is_mentioned = 1 if status.lower() in ("mentioned", "cited") or self.detect_brand_mention(summary) else 0
        is_cited = 1 if status.lower() == "cited" else 0

        return {
            "response_id": f"RESP-{question_id}-D{day_number}-CLAUDE",
            "question_id": question_id,
            "provider": self.provider_name,
            "model_version": engine,
            "checked_at": ts,
            "market": evidence.get("market", "US"),
            "location_setting": meta.get("ip_location", "GeoIP: US"),
            "status_declared": status,
            "competitors_mentioned": comps,
            "citation_urls": ai_sec.get("cited_urls", []),
            "raw_response_text": summary,
            "response_hash": self.compute_sha256(summary or f"{question_id}-claude"),
            "incubrix_mentioned": is_mentioned,
            "incubrix_cited": is_cited,
            "collection_status": "Success" if summary else "Missing",
            "error_message": None
        }
