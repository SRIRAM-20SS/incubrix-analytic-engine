"""
IncuBrix Content Engine: Topic Selector (Phase 4)
Selects and prioritizes 10 target topics based on Phase 1 questions and Phase 2 visibility baseline.
Enforces balanced mix: How-to guides, comparisons, FAQs, glossary, and creator workflow guides.
"""

from typing import List, Dict, Any
import pandas as pd
import os

SELECTED_TOPICS: List[Dict[str, Any]] = [
    {
        "page_id": "P01",
        "slug": "turn-long-videos-into-shorts-ai",
        "full_url": "https://incubrix.com/guides/turn-long-videos-into-shorts-ai",
        "primary_question": "How do I turn long videos into shorts with AI?",
        "target_question_ids": ["Q021", "Q025"],
        "category": "Content repurposing",
        "content_type": "How-to Guide",
        "target_opportunity": "OPP-01",
        "search_intent": "Informational / Practical How-To",
        "target_audience": "Solo video creators, YouTubers, and social media managers looking to scale vertical output.",
        "primary_keyword": "turn long videos into shorts ai",
        "secondary_keywords": ["ai video repurposing", "convert youtube video to shorts", "auto clip long videos"],
        "selection_rationale": (
            "Directly targets IncuBrix's core AI vertical repurposing engine. Q021 exhibits massive search demand "
            "across Google and Reddit, with 62% AI Overview triggering rate. IncuBrix currently has 0% organic visibility "
            "while OpusClip dominates (47% SoV). Provides a step-by-step technical guide with immediate product trial CTA."
        ),
        "competition_level": "High (dominated by OpusClip and Klap)",
        "visibility_gap": "IncuBrix unranked (>100) on Google, 0 mentions in ChatGPT/Claude",
        "conversion_potential": "High (direct software trial on app.incubrix.com with 300 free credits)"
    },
    {
        "page_id": "P02",
        "slug": "podcast-video-repurposing-guide",
        "full_url": "https://incubrix.com/workflows/podcast-video-repurposing-guide",
        "primary_question": "How do podcasters create viral TikTok clips and Reels automatically?",
        "target_question_ids": ["Q022", "Q026"],
        "category": "Content repurposing",
        "content_type": "Practical Creator Workflow Guide",
        "target_opportunity": "OPP-01",
        "search_intent": "Commercial Investigation / Practical Workflow Guide",
        "target_audience": "Audio & video podcast hosts, producers, and media networks wanting multi-channel clips.",
        "primary_keyword": "podcast video repurposing guide",
        "secondary_keywords": ["podcast clips for tiktok", "turn podcast into reels", "podcast video clipper"],
        "selection_rationale": (
            "Podcasters generate the highest volume of long-form audio/video content (60-90 min episodes). Q022 and Q026 "
            "represent frequent PAA queries. Capturing podcasters drives high credit consumption (~14 credits/min of video). "
            "Workflow guide details transcript analysis, speaker framing, and multi-clip batch generation."
        ),
        "competition_level": "Medium-High (Descript, Podsqueeze, OpusClip)",
        "visibility_gap": "IncuBrix unranked, zero citations across US/UK/IN AI queries",
        "conversion_potential": "Very High (recurring weekly production workflow)"
    },
    {
        "page_id": "P03",
        "slug": "opusclip-alternatives",
        "full_url": "https://incubrix.com/comparisons/opusclip-alternatives",
        "primary_question": "What are the best OpusClip alternatives for AI video clipping in 2026?",
        "target_question_ids": ["Q041", "Q047"],
        "category": "Product comparisons",
        "content_type": "Comparison Article",
        "target_opportunity": "OPP-02",
        "search_intent": "Commercial Investigation / High-Intent Comparison",
        "target_audience": "Creators and agencies dissatisfied with OpusClip pricing, credit limits, or caption styling.",
        "primary_keyword": "opusclip alternatives",
        "secondary_keywords": ["best ai video clipping tools", "opus clip alternative free", "tools like opus clip"],
        "selection_rationale": (
            "Phase 2 baseline revealed OpusClip holds 47% share of voice across AI assistants. Bidding or ranking for "
            "'OpusClip alternatives' captures bottom-of-funnel creators ready to switch. Features an objective, factual "
            "comparison matrix covering credit economics, multi-speaker face tracking, and unified publishing."
        ),
        "competition_level": "High (G2, Capterra, niche review blogs)",
        "visibility_gap": "IncuBrix absent from all 5 comparison lists in AI baseline",
        "conversion_potential": "Maximum (active software buyers comparing pricing tiers)"
    },
    {
        "page_id": "P04",
        "slug": "alex-hormozi-style-captions",
        "full_url": "https://incubrix.com/guides/alex-hormozi-style-captions",
        "primary_question": "How do I create animated captions with emoji like Alex Hormozi?",
        "target_question_ids": ["Q061", "Q062"],
        "category": "Caption generation",
        "content_type": "How-to Guide",
        "target_opportunity": "OPP-01",
        "search_intent": "Informational / Practical How-To",
        "target_audience": "Short-form video editors, business influencers, and TikTok/Reels creators.",
        "primary_keyword": "alex hormozi style captions",
        "secondary_keywords": ["animated captions generator", "tiktok caption styles", "auto captions with emojis"],
        "selection_rationale": (
            "High viral search volume query. Q061 is one of the most frequently asked styling questions in creator forums. "
            "IncuBrix provides built-in word-by-word active karaoke highlighting and auto-emoji placement. Delivering a direct "
            "2-sentence answer secures Google Featured Snippets."
        ),
        "competition_level": "Medium (Submagic, CapCut tutorials)",
        "visibility_gap": "IncuBrix unranked; Submagic dominates search results",
        "conversion_potential": "High (creators immediately test caption presets in studio)"
    },
    {
        "page_id": "P05",
        "slug": "descript-vs-incubrix",
        "full_url": "https://incubrix.com/comparisons/descript-vs-incubrix",
        "primary_question": "Descript vs IncuBrix: Which is better for multi-platform video repurposing?",
        "target_question_ids": ["Q042", "Q044"],
        "category": "Product comparisons",
        "content_type": "Comparison Article",
        "target_opportunity": "OPP-02",
        "search_intent": "Commercial Investigation / Head-to-Head Comparison",
        "target_audience": "Video editors evaluating text-based NLEs vs dedicated end-to-end CreatorOps platforms.",
        "primary_keyword": "descript vs incubrix",
        "secondary_keywords": ["descript alternatives", "text based video editing vs ai clipping", "descript pricing"],
        "selection_rationale": (
            "Descript is the second largest competitor in our Phase 2 baseline (44% SoV). Descript excels at desktop "
            "podcast editing but requires manual timeline exports and lacks native multi-platform social scheduling. "
            "This head-to-head comparison establishes IncuBrix's positioning as the integrated CreatorOps alternative."
        ),
        "competition_level": "Medium (brand comparison searches)",
        "visibility_gap": "IncuBrix unmentioned in AI responses comparing Descript",
        "conversion_potential": "Very High (positions IncuBrix alongside category leader)"
    },
    {
        "page_id": "P06",
        "slug": "reframe-horizontal-video-to-vertical-9-16",
        "full_url": "https://incubrix.com/guides/reframe-horizontal-video-to-vertical-9-16",
        "primary_question": "How do I reframe 16:9 horizontal videos to 9:16 vertical without cropping the speaker?",
        "target_question_ids": ["Q011", "Q013"],
        "category": "Video and content editing",
        "content_type": "How-to Guide",
        "target_opportunity": "OPP-01",
        "search_intent": "Technical / Practical How-To",
        "target_audience": "Premiere/DaVinci editors and automated video producers struggling with manual keyframing.",
        "primary_keyword": "reframe horizontal video to vertical 9 16",
        "secondary_keywords": ["auto reframe video ai", "convert 16:9 to 9:16", "speaker tracking video crop"],
        "selection_rationale": (
            "Manual center-cropping cuts off moving speakers and multi-person interviews. Q011 and Q013 address "
            "computer vision face detection and active speaker diarization. IncuBrix's automated 9:16 crop engine "
            "directly solves this technical pain point."
        ),
        "competition_level": "Medium (Adobe Premiere Auto Reframe documentation)",
        "visibility_gap": "IncuBrix unranked for aspect ratio conversion queries",
        "conversion_potential": "High (solves a tedious 45-minute manual editing task in seconds)"
    },
    {
        "page_id": "P07",
        "slug": "ai-video-editing-faq-troubleshooting",
        "full_url": "https://incubrix.com/resources/ai-video-editing-faq-troubleshooting",
        "primary_question": "Why are my AI generated video clips blurry or out of sync?",
        "target_question_ids": ["Q014", "Q018", "Q028"],
        "category": "Video and content editing",
        "content_type": "FAQ & Troubleshooting Guide",
        "target_opportunity": "OPP-03",
        "search_intent": "Informational / Technical Troubleshooting & FAQ",
        "target_audience": "Creators encountering audio drift, bitrate compression, or export rendering glitches.",
        "primary_keyword": "ai video editing troubleshooting faq",
        "secondary_keywords": ["ai clips out of sync", "fix blurry vertical video", "audio drift ai video editor"],
        "selection_rationale": (
            "Troubleshooting questions trigger high Answer Engine and PAA inclusion rates. Q014, Q018, and Q028 "
            "represent creators troubleshooting frame rate mismatches (VFR vs CFR), audio sample rates (44.1kHz vs 48kHz), "
            "and bitrates. Structured FAQPage schema qualifies for Google SERP rich accordions."
        ),
        "competition_level": "Low-Medium (scattered Reddit threads and support docs)",
        "visibility_gap": "IncuBrix has 0 FAQPage schemas on live domain (identified in Phase 3)",
        "conversion_potential": "Medium-High (builds authoritative domain trust and technical credibility)"
    },
    {
        "page_id": "P08",
        "slug": "schedule-shorts-reels-tiktok-single-dashboard",
        "full_url": "https://incubrix.com/workflows/schedule-shorts-reels-tiktok-single-dashboard",
        "primary_question": "How do I schedule YouTube Shorts, Instagram Reels, and TikTok from one place?",
        "target_question_ids": ["Q071", "Q075"],
        "category": "Publishing workflows",
        "content_type": "Practical Creator Workflow Guide",
        "target_opportunity": "OPP-01",
        "search_intent": "Commercial / Workflow Automation",
        "target_audience": "Multi-platform creators, digital brands, and social media managers.",
        "primary_keyword": "schedule shorts reels tiktok one place",
        "secondary_keywords": ["multi platform video scheduler", "cross post vertical video", "auto publish shorts and reels"],
        "selection_rationale": (
            "Eliminates the 'tool fatigue' of downloading clips from an editor and re-uploading to Buffer/Hootsuite. "
            "IncuBrix unifies AI clipping with direct social API publishing (YouTube, TikTok, Instagram, LinkedIn). "
            "Captures creators seeking an end-to-end publishing pipeline."
        ),
        "competition_level": "Medium-High (Buffer, Later, Metricool)",
        "visibility_gap": "IncuBrix publishing capabilities invisible in AI assistant baselines",
        "conversion_potential": "Very High (unifies editing and distribution in one subscription)"
    },
    {
        "page_id": "P09",
        "slug": "what-is-creatorops-creator-operating-system",
        "full_url": "https://incubrix.com/glossary/what-is-creatorops-creator-operating-system",
        "primary_question": "What is CreatorOps (Creator Operating System) and how does it work?",
        "target_question_ids": ["Q051", "Q091"],
        "category": "Workflow automation",
        "content_type": "Glossary or Explanatory Page",
        "target_opportunity": "OPP-03",
        "search_intent": "Informational / Conceptual Framework & Glossary",
        "target_audience": "Creator economy founders, agency leads, industry analysts, and modern media companies.",
        "primary_keyword": "what is creatorops creator operating system",
        "secondary_keywords": ["creatorops definition", "creator operating system", "content production pipeline ai"],
        "selection_rationale": (
            "Category creation and thought leadership. IncuBrix defines itself as 'The AI-powered operating system "
            "for the creator economy (CreatorOps)'. Establishes the formal definition of CreatorOps across the 5 lifecycle "
            "stages (Discover -> Create -> Repurpose -> Publish -> Learn) for Perplexity and LLM knowledge graphs."
        ),
        "competition_level": "Low (emerging category term, ripe for definition ownership)",
        "visibility_gap": "No indexed canonical definition of CreatorOps on Google",
        "conversion_potential": "High (positions IncuBrix as the category pioneer and enterprise standard)"
    },
    {
        "page_id": "P10",
        "slug": "ai-video-repurposing-for-agencies",
        "full_url": "https://incubrix.com/solutions/ai-video-repurposing-for-agencies",
        "primary_question": "What is the best AI video repurposing workflow for social media agencies?",
        "target_question_ids": ["Q048", "Q095"],
        "category": "Workflow automation",
        "content_type": "Practical Creator Workflow Guide",
        "target_opportunity": "OPP-02",
        "search_intent": "Commercial / B2B Agency Evaluation",
        "target_audience": "B2B social media agency owners, client managers, and creative directors.",
        "primary_keyword": "ai video repurposing for agencies",
        "secondary_keywords": ["agency video editing workflow", "bulk video clipping for clients", "white label video repurposing"],
        "selection_rationale": (
            "Agencies drive the highest lifetime customer value (LTV) and consume top pricing tiers (Growth $50, "
            "Scale $100, Pro $250/mo). Q048 and Q095 focus on multi-client workspaces, credit pooling, and batch exports. "
            "Provides an agency ROI calculator framework and step-by-step client onboarding."
        ),
        "competition_level": "Medium (general agency blogs)",
        "visibility_gap": "IncuBrix absent from B2B agency tool roundups",
        "conversion_potential": "Maximum (high-ticket enterprise/agency signups on app.incubrix.com)"
    }
]


class TopicSelector:
    """Manages the selection, validation, and export of Phase 4 target topics."""

    @staticmethod
    def get_all_topics() -> List[Dict[str, Any]]:
        return SELECTED_TOPICS

    @staticmethod
    def get_topic_by_id(page_id: str) -> Dict[str, Any]:
        for t in SELECTED_TOPICS:
            if t["page_id"].upper() == page_id.upper():
                return t
        raise KeyError(f"Topic ID {page_id} not found in SELECTED_TOPICS.")

    @staticmethod
    def validate_topic_mix() -> Dict[str, Any]:
        """Validates that the 10 topics meet assessment diversity criteria."""
        topics = SELECTED_TOPICS
        types = [t["content_type"] for t in topics]
        categories = [t["category"] for t in topics]
        opportunities = [t["target_opportunity"] for t in topics]

        return {
            "total_topics": len(topics),
            "content_types_count": len(set(types)),
            "content_types": pd.Series(types).value_counts().to_dict(),
            "categories_covered": len(set(categories)),
            "opportunities_covered": sorted(list(set(opportunities))),
            "is_valid": len(topics) == 10 and len(set(types)) >= 4 and len(set(opportunities)) == 3
        }


if __name__ == "__main__":
    validation = TopicSelector.validate_topic_mix()
    print("Topic Selector Validation:")
    print(validation)
