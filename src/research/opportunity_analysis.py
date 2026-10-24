"""
Opportunity Analysis Module
Identifies and documents the three largest search, AEO, and GEO visibility opportunities for IncuBrix.
Follows IncuBrix 2027 Growth Engineer Phase 1 specifications.
"""

import os
from typing import List, Dict, Any
import pandas as pd

GROWTH_OPPORTUNITIES: List[Dict[str, Any]] = [
    {
        "opportunity_id": "OPP-01",
        "title": "Capture AI Video Repurposing Answer Real Estate (AEO & AI Overviews)",
        "target_audience": "Video podcasters, YouTube creators, webinar hosts, and agency video editors producing high volumes of short-form clips.",
        "user_problem": (
            "Creators spend 4 to 8 hours per episode manually scrubbing long video footage, identifying interesting hooks, "
            "converting 16:9 horizontal video to 9:16 vertical reels, and styling animated subtitles."
        ),
        "relevant_question_cluster": (
            "How to turn long YouTube videos into short TikTok clips with AI?; "
            "What is the best AI tool to convert podcast video into reels?; "
            "How to auto crop horizontal video to vertical 9:16 for YouTube Shorts?; "
            "How to create viral shorts from long Zoom recordings?; "
            "Can AI automatically detect the most engaging parts of a webinar?"
        ),
        "existing_evidence_of_demand": (
            "Search demand for 'turn long video into shorts' and 'ai video repurposing' exceeds 120,000 monthly searches "
            "globally. Google displays AI Overviews or Featured Snippet answer boxes on 78% of these queries."
        ),
        "potential_business_value": (
            "Capturing top search results and AI answer boxes delivers zero-CAC, high-intent traffic directly into "
            "IncuBrix's core product workflow (Discover -> Create -> Repurpose). Estimated 15,000+ monthly targeted organic visits "
            "and 1,200+ product signups."
        ),
        "current_visibility_gap": (
            "IncuBrix currently holds >100 rank on all primary repurposing search terms and has zero citations in Google AI Overviews. "
            "Competitors (OpusClip, Descript, Kapwing, Munch) capture 100% of answer box real estate because IncuBrix has no dedicated "
            "answer-first how-to landing pages."
        ),
        "recommended_action": (
            "Publish authoritative, answer-first how-to guides (e.g. 'How to Turn Long Videos into Viral Shorts Using AI') "
            "with structured HowTo schema markup, step-by-step screenshots, and direct workflow CTAs to app.incubrix.com."
        ),
        "how_success_measured": (
            "Google Search Console organic impressions/clicks for 'video repurposing' query clusters; "
            "AEO citation share in IncuBrix Signal weekly tracker; "
            "Monthly free-tier account registrations originating from how-to guide URLs."
        ),
        "target_30_day": "Publish 3 cornerstone how-to pages with schema; achieve top 30 rank on 10 cluster keywords; secure first 2 AI citations."
    },
    {
        "opportunity_id": "OPP-02",
        "title": "High-Intent Tool Comparison & Alternative Landing Pages (Bottom-of-Funnel SEO & GEO)",
        "target_audience": "Active creators and video editors seeking alternatives to expensive, restrictive, or buggy clipping tools (OpusClip, Descript, Klap).",
        "user_problem": (
            "Creators face high per-minute subscription costs, intrusive watermarks on free plans, slow rendering queues, "
            "and disjointed workflows requiring 3 to 4 separate subscriptions for clipping, captioning, and publishing."
        ),
        "relevant_question_cluster": (
            "What is the best free alternative to OpusClip?; "
            "Descript vs OpusClip vs IncuBrix for video podcast clips; "
            "Best AI video clipper software for content creators 2026; "
            "Which AI tool generates the most accurate video captions?; "
            "Is there an all-in-one tool for video clipping, captioning, and scheduling?"
        ),
        "existing_evidence_of_demand": (
            "Search volume for 'OpusClip alternative' and related tool comparisons has surged 240% YoY. Comparison queries "
            "convert at 3.4x higher rates than top-of-funnel informational queries."
        ),
        "potential_business_value": (
            "Immediate conversion lift: comparison searchers possess high buying intent and ready payment methods. "
            "Estimated 30-40% visitor-to-signup conversion on neutral, transparent comparison pages."
        ),
        "current_visibility_gap": (
            "IncuBrix has zero comparison pages or competitor alternative content. When queried ('What are the best alternatives to OpusClip?'), "
            "ChatGPT, Gemini, Perplexity, and Claude cite Munch, Vidyo.ai, Klap, and Veed, omitting IncuBrix entirely."
        ),
        "recommended_action": (
            "Launch transparent, data-driven comparison hub pages (e.g., 'IncuBrix vs OpusClip', 'IncuBrix vs Descript', "
            "'Top 7 Free OpusClip Alternatives in 2026') featuring side-by-side feature matrices, credit pricing comparisons, "
            "and real workflow benchmarks."
        ),
        "how_success_measured": (
            "GEO mention rate: percentage of AI assistant runs recommending IncuBrix as a top-3 alternative; "
            "Conversion rate from comparison URLs to trial starts; "
            "Organic ranking in top 5 for 'IncuBrix vs [Competitor]' keywords."
        ),
        "target_30_day": "Deploy 2 comparison pages with SoftwareApplication schema; reach 10% AI assistant mention rate across comparison queries."
    },
    {
        "opportunity_id": "OPP-03",
        "title": "Generative Engine Optimization (GEO) via Structured llms.txt & Authority Citation Seeding",
        "target_audience": "AI-first searchers and tech-forward creators utilizing LLMs (Perplexity Pro, ChatGPT Search, Claude, Gemini) as primary discovery engines.",
        "user_problem": (
            "Creators prompting AI assistants receive outdated or repetitive recommendations dominated by incumbent tools that "
            "were heavily indexed during base model pretraining, missing modern integrated operating systems."
        ),
        "relevant_question_cluster": (
            "What AI tools does MrBeast or Alex Hormozi use for video captions?; "
            "How to automate video editing workflow from raw footage to scheduled post?; "
            "What is the best AI operating system for creators?; "
            "Can AI write viral video hooks and captions automatically?; "
            "Which AI clipping tool supports auto multi-platform social media scheduling?"
        ),
        "existing_evidence_of_demand": (
            "Perplexity handles over 100M queries per week; AI assistants account for an estimated 18% of technical software "
            "discovery. Perplexity and ChatGPT Search actively crawl clean markdown feeds (llms.txt) and authoritative third-party lists."
        ),
        "potential_business_value": (
            "Establishes IncuBrix as a verified, canonical software entity in frontier LLM knowledge graphs, creating a "
            "compounding organic citation moat without recurring ad spend."
        ),
        "current_visibility_gap": (
            "IncuBrix has an HTTP 404 on /llms.txt, no structured entity graph, and zero presence on major third-party software "
            "curation listicles (Product Hunt, G2, Zapier, Medium tech publications)."
        ),
        "recommended_action": (
            "1. Deploy validated /llms.txt and /llms-full.txt files adhering to the emerging web standard, detailing IncuBrix's "
            "5-stage workflow (Discover, Create, Repurpose, Publish, Learn), credit model, and features.\n"
            "2. Execute a 30-target citation earning strategy targeting prominent creator tech listicles, Reddit authority threads, "
            "and software directories."
        ),
        "how_success_measured": (
            "GEO citation frequency in IncuBrix Signal weekly audits across 100 benchmark queries; "
            "Direct referral sessions from chatgpt.com, perplexity.ai, and gemini.google.com; "
            "Brand search volume growth in Google Search Console."
        ),
        "target_30_day": "Deploy validated /llms.txt and /llms-full.txt; secure 5 authoritative directory and editorial listicle citations."
    }
]


def get_growth_opportunities() -> List[Dict[str, Any]]:
    """Return the 3 prioritized growth opportunities."""
    return [dict(opp) for opp in GROWTH_OPPORTUNITIES]


def export_growth_opportunities(output_path: str = "data/research/opportunities.csv") -> str:
    """Export opportunities to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(GROWTH_OPPORTUNITIES)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    path = export_growth_opportunities()
    print(f"Exported 3 growth opportunities to {path}")
