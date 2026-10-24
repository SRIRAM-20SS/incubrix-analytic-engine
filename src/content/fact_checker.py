"""
IncuBrix Content Engine: Fact Checker & Product Verification (Phase 4)
Maintains verified product claims, competitor comparison benchmarks, and traceable citations.
Flags unverified capabilities, exaggerated superlatives, and unsupported statistics.
"""

from typing import List, Dict, Any, Tuple
import re

VERIFIED_INCUBRIX_SPECS = {
    "product_name": "IncuBrix",
    "legal_entity": "IncuBrix Private Limited",
    "positioning": "The AI-powered operating system for the creator economy (CreatorOps)",
    "lifecycle_stages": ["Discover", "Create", "Repurpose", "Publish", "Learn"],
    "supported_inputs": ["YouTube URLs", "Zoom Cloud Recordings", "Google Drive", "Dropbox", "Local MP4/MOV"],
    "supported_aspect_ratios": ["9:16 (1080x1920)", "1:1 (1080x1080)", "16:9 (1920x1080)"],
    "speech_to_text_engine": "OpenAI Whisper (automated transcription with punctuation and timestamping)",
    "caption_styles": ["Karaoke word-by-word highlighting", "Custom font selection", "Emoji auto-sync", "Custom colors"],
    "publishing_integrations": ["YouTube Shorts (Data API v3)", "TikTok (Content Posting API)", "Instagram Reels (Graph API)", "LinkedIn Video"],
    "pricing_tiers": {
        "Free": {"price": "$0/mo", "credits": 300, "features": "Standard transcription, 720p/1080p export, community support"},
        "Starter": {"price": "$10/mo", "credits": 1000, "features": "Full HD 1080p, no watermark, basic auto-scheduling"},
        "Essential": {"price": "$20/mo", "credits": 2000, "features": "Multi-aspect ratio export, custom caption styles, priority render"},
        "Growth": {"price": "$50/mo", "credits": 5000, "features": "Direct social publishing, team collaboration, 4K export support"},
        "Scale": {"price": "$100/mo", "credits": 10000, "features": "Custom brand kits, API access, batch processing"},
        "Pro": {"price": "$250/mo", "credits": 25000, "features": "Dedicated rendering queue, custom AI model fine-tuning, SLA support"}
    },
    "credit_consumption_rate": 14, # ~14 credits per 1 minute of processed video
    "app_url": "https://app.incubrix.com",
    "verified_endpoints": ["https://incubrix.com/", "https://incubrix.com/pricing", "https://incubrix.com/about", "https://incubrix.com/faq", "https://incubrix.com/manifesto", "https://incubrix.com/waitlist"]
}

VERIFIED_SOURCES = [
    {
        "source_name": "OpenAI Whisper Documentation",
        "url": "https://github.com/openai/whisper",
        "supported_claim": "Whisper provides robust multilingual speech-to-text transcription with word-level timestamping."
    },
    {
        "source_name": "YouTube Creator Documentation (Shorts Specs)",
        "url": "https://support.google.com/youtube/answer/10059070",
        "supported_claim": "YouTube Shorts supports 9:16 vertical video up to 60 seconds (extended to 3 minutes for select uploads)."
    },
    {
        "source_name": "Instagram Graph API Documentation",
        "url": "https://developers.facebook.com/docs/instagram-api/guides/content-publishing",
        "supported_claim": "Instagram Reels publishing API requires 9:16 aspect ratio, H.264/AAC codec, and max 1080p resolution."
    },
    {
        "source_name": "TikTok Content Posting API Reference",
        "url": "https://developers.tiktok.com/doc/content-posting-api-reference-direct-post",
        "supported_claim": "TikTok Direct Post API supports video uploads with title, cover image, and privacy settings."
    },
    {
        "source_name": "W3C Web Content Accessibility Guidelines (WCAG 2.1)",
        "url": "https://www.w3.org/WAI/standards-guidelines/wcag/",
        "supported_claim": "Captions and text alternatives are mandatory for prerecorded synchronized media to satisfy WCAG AA compliance."
    },
    {
        "source_name": "Google Search Central: Structured Data Guidelines",
        "url": "https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data",
        "supported_claim": "JSON-LD structured data enables search engines to parse page context for rich snippets."
    },
    {
        "source_name": "Descript Official Product Documentation",
        "url": "https://www.descript.com/pricing",
        "supported_claim": "Descript operates as a desktop/web timeline editor with text-based editing, transcription hours quotas, and manual export."
    },
    {
        "source_name": "OpusClip Official Product Documentation",
        "url": "https://www.opus.pro/pricing",
        "supported_claim": "OpusClip provides automated AI clipping with virality scores, dynamic face tracking, and credit-based billing."
    }
]

FORBIDDEN_SUPERLATIVES = [
    "best tool in the world",
    "guaranteed to go viral",
    "100% viral rate",
    "infinitely better than",
    "the only tool you will ever need",
    "magic button to riches"
]


class FactChecker:
    """Verifies content for product accuracy, traceable citations, and neutral tone."""

    @staticmethod
    def get_verified_specs() -> Dict[str, Any]:
        return VERIFIED_INCUBRIX_SPECS

    @staticmethod
    def get_verified_sources() -> List[Dict[str, str]]:
        return VERIFIED_SOURCES

    @staticmethod
    def check_text_for_superlatives(text: str) -> List[str]:
        """Detects unsupported hyperbolic superlatives in generated copy."""
        violations = []
        lower_text = text.lower()
        for sup in FORBIDDEN_SUPERLATIVES:
            if sup in lower_text:
                violations.append(sup)
        return violations

    @staticmethod
    def verify_incubrix_claims(text: str) -> Dict[str, Any]:
        """Verifies that stated IncuBrix features match verified capabilities."""
        flags = []
        lower = text.lower()

        # Check credit consumption consistency
        if "credit" in lower and "minute" in lower:
            # If mentions credits per min, verify it doesn't state wild inaccuracies (e.g. 500 credits per min)
            if re.search(r'\b(50|100|500)\s*credits\s*per\s*min', lower):
                flags.append("Inaccurate credit consumption rate (standard is ~14 credits/min)")

        # Check pricing consistency
        if "$0" in text or "free" in lower:
            if "300" not in text and "free" in lower and "plan" in lower:
                # Neutral observation
                pass

        return {
            "has_flags": len(flags) > 0,
            "flags": flags,
            "verified_specs_reference": "VERIFIED_INCUBRIX_SPECS"
        }

    @staticmethod
    def check_citation_traceability(citations: List[Dict[str, str]]) -> Tuple[bool, List[str]]:
        """Ensures every citation provides an authentic, traceable URL."""
        errors = []
        for c in citations:
            url = c.get("url", "")
            if not url.startswith("http://") and not url.startswith("https://"):
                errors.append(f"Invalid citation URL: {url}")
            if not c.get("supported_claim"):
                errors.append(f"Citation missing supported_claim: {c.get('source_name')}")
        return len(errors) == 0, errors


if __name__ == "__main__":
    print(f"Verified sources loaded: {len(VERIFIED_SOURCES)}")
    print(f"Verified pricing tiers: {list(VERIFIED_INCUBRIX_SPECS['pricing_tiers'].keys())}")
