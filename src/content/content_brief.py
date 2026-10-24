"""
IncuBrix Content Engine: Content Brief Generator (Phase 4)
Generates structured editorial briefs for writers and automation engines.
Enforces Answer-First architecture (direct answer in opening 2 sentences), factual backing, and schema mapping.
"""

from typing import Dict, Any, List
from src.content.topic_selector import TopicSelector
from src.content.internal_links import InternalLinkManager
from src.content.fact_checker import FactChecker


class ContentBriefGenerator:
    """Creates standardized content briefs for all 10 Phase 4 target pages."""

    @classmethod
    def generate_brief_for_topic(cls, page_id: str) -> Dict[str, Any]:
        topic = TopicSelector.get_topic_by_id(page_id)
        internal_links = InternalLinkManager.get_contextual_links_for_page(page_id)
        verified_specs = FactChecker.get_verified_specs()

        brief = {
            "page_id": topic["page_id"],
            "slug": topic["slug"],
            "full_url": topic["full_url"],
            "primary_question": topic["primary_question"],
            "target_question_ids": topic["target_question_ids"],
            "category": topic["category"],
            "content_type": topic["content_type"],
            "target_opportunity": topic["target_opportunity"],
            "search_intent": topic["search_intent"],
            "target_audience": topic["target_audience"],
            "primary_keyword": topic["primary_keyword"],
            "secondary_keywords": topic["secondary_keywords"],
            "selection_rationale": topic["selection_rationale"],
            "direct_answer_requirement": (
                "MUST answer the core question concisely in the very first 2 sentences. "
                "No introductory filler, rhetorical questions, or historical preamble. "
                "Optimized for Google AI Overviews and Perplexity extraction."
            ),
            "verified_product_anchors": {
                "positioning": verified_specs["positioning"],
                "credit_consumption": "~14 credits per 1 minute of processed video",
                "free_tier": "Free plan includes 300 credits with no credit card required",
                "app_url": verified_specs["app_url"]
            },
            "internal_links": internal_links,
            "required_schema_types": (
                ["Article", "BreadcrumbList", "HowTo"] if "How-to" in topic["content_type"] or "Workflow" in topic["content_type"]
                else ["Article", "BreadcrumbList", "FAQPage"] if "FAQ" in topic["content_type"]
                else ["Article", "BreadcrumbList", "SoftwareApplication"]
            ),
            "editorial_checklist": [
                "Direct answer present in first 2 sentences",
                "All factual claims backed by traceable URLs",
                "IncuBrix product features match verified specs",
                "No unsupported superlatives or viral guarantees",
                "Descriptive anchor text on all internal links",
                "JSON-LD structured data validated without errors"
            ]
        }
        return brief

    @classmethod
    def generate_all_briefs(cls) -> List[Dict[str, Any]]:
        topics = TopicSelector.get_all_topics()
        return [cls.generate_brief_for_topic(t["page_id"]) for t in topics]


if __name__ == "__main__":
    brief = ContentBriefGenerator.generate_brief_for_topic("P01")
    print(f"Generated Content Brief for {brief['page_id']}: {brief['primary_question']}")
    print("Direct answer constraint:", brief["direct_answer_requirement"])
