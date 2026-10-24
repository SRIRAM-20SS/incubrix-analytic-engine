"""
IncuBrix Content Engine: Internal Links Directory (Phase 4)
Manages verified site-wide internal link targets and cross-page recommendations.
Ensures high-relevance internal linking using descriptive keyword anchor text.
"""

from typing import List, Dict, Any

VERIFIED_SITE_PAGES = {
    "home": {
        "url": "https://incubrix.com/",
        "recommended_anchors": ["IncuBrix AI CreatorOps platform", "IncuBrix homepage", "AI video operating system"]
    },
    "pricing": {
        "url": "https://incubrix.com/pricing",
        "recommended_anchors": ["IncuBrix pricing plans", "view credit tiers and pricing", "compare subscription tiers"]
    },
    "about": {
        "url": "https://incubrix.com/about",
        "recommended_anchors": ["about IncuBrix", "our company story", "IncuBrix CreatorOps vision"]
    },
    "faq": {
        "url": "https://incubrix.com/faq",
        "recommended_anchors": ["frequently asked questions", "IncuBrix creator FAQ", "video processing knowledgebase"]
    },
    "manifesto": {
        "url": "https://incubrix.com/manifesto",
        "recommended_anchors": ["IncuBrix Creator Manifesto", "our creator-first philosophy", "the CreatorOps manifesto"]
    },
    "waitlist": {
        "url": "https://incubrix.com/waitlist",
        "recommended_anchors": ["join early access waitlist", "request early beta access", "IncuBrix waitlist"]
    },
    "studio_app": {
        "url": "https://app.incubrix.com",
        "recommended_anchors": ["start free in IncuBrix Studio", "launch IncuBrix Web App", "claim 300 free credits"]
    }
}


class InternalLinkManager:
    """Provides verified internal link targets and contextual recommendations for Phase 4 pages."""

    @staticmethod
    def get_verified_urls() -> List[str]:
        return [p["url"] for p in VERIFIED_SITE_PAGES.values()]

    @staticmethod
    def get_contextual_links_for_page(page_id: str) -> List[Dict[str, str]]:
        """Returns 3-4 highly relevant internal links for each specific page ID."""
        link_matrix = {
            "P01": [
                {"anchor": "claim 300 free credits in IncuBrix Studio", "url": "https://app.incubrix.com", "context": "Try the automated video repurposing tool directly."},
                {"anchor": "compare credit tiers and pricing", "url": "https://incubrix.com/pricing", "context": "See pricing details for Starter, Essential, and Growth plans."},
                {"anchor": "podcast video repurposing guide", "url": "https://incubrix.com/workflows/podcast-video-repurposing-guide", "context": "Learn how to batch process full podcast episodes."},
                {"anchor": "Alex Hormozi style animated captions", "url": "https://incubrix.com/guides/alex-hormozi-style-captions", "context": "Add viral word-by-word animated subtitles."}
            ],
            "P02": [
                {"anchor": "start free in IncuBrix Studio", "url": "https://app.incubrix.com", "context": "Upload your podcast audio or video file."},
                {"anchor": "IncuBrix pricing plans", "url": "https://incubrix.com/pricing", "context": "Review credit packages (~14 credits/min of video)."},
                {"anchor": "reframe 16:9 horizontal videos to vertical 9:16", "url": "https://incubrix.com/guides/reframe-horizontal-video-to-vertical-9-16", "context": "Automatically detect and frame active speakers."},
                {"anchor": "multi-platform publishing workflow", "url": "https://incubrix.com/workflows/schedule-shorts-reels-tiktok-single-dashboard", "context": "Distribute clips to YouTube, TikTok, and Instagram."}
            ],
            "P03": [
                {"anchor": "test IncuBrix CreatorOps Studio free", "url": "https://app.incubrix.com", "context": "Get 300 free credits with zero credit card required."},
                {"anchor": "IncuBrix subscription tiers", "url": "https://incubrix.com/pricing", "context": "Compare our $10-$250 monthly plans vs competitor pricing."},
                {"anchor": "Descript vs IncuBrix comparison", "url": "https://incubrix.com/comparisons/descript-vs-incubrix", "context": "Explore text-based editing vs dedicated repurposing."},
                {"anchor": "IncuBrix Creator Manifesto", "url": "https://incubrix.com/manifesto", "context": "Read why we built a unified Creator Operating System."}
            ],
            "P04": [
                {"anchor": "create animated captions in IncuBrix Studio", "url": "https://app.incubrix.com", "context": "Test automated emoji sync and karaoke highlighting."},
                {"anchor": "IncuBrix creator FAQ", "url": "https://incubrix.com/faq", "context": "Answers to subtitle timing and export settings."},
                {"anchor": "turn long videos into shorts with AI", "url": "https://incubrix.com/guides/turn-long-videos-into-shorts-ai", "context": "Complete video repurposing walkthrough."}
            ],
            "P05": [
                {"anchor": "try IncuBrix Studio with 300 free credits", "url": "https://app.incubrix.com", "context": "Experience automated AI clipping with zero download."},
                {"anchor": "IncuBrix pricing plans", "url": "https://incubrix.com/pricing", "context": "Check our Starter ($10/mo) and Growth ($50/mo) packages."},
                {"anchor": "best OpusClip alternatives in 2026", "url": "https://incubrix.com/comparisons/opusclip-alternatives", "context": "Examine top clipping tools on the market."},
                {"anchor": "what is CreatorOps?", "url": "https://incubrix.com/glossary/what-is-creatorops-creator-operating-system", "context": "Understand the 5 stages of creator workflow."}
            ],
            "P06": [
                {"anchor": "launch IncuBrix Web App", "url": "https://app.incubrix.com", "context": "Upload horizontal footage and test auto-reframing."},
                {"anchor": "AI video editing troubleshooting FAQ", "url": "https://incubrix.com/resources/ai-video-editing-faq-troubleshooting", "context": "Solve audio sync, blurriness, and aspect ratio issues."},
                {"anchor": "podcast video repurposing guide", "url": "https://incubrix.com/workflows/podcast-video-repurposing-guide", "context": "Frame multi-speaker video interviews seamlessly."}
            ],
            "P07": [
                {"anchor": "IncuBrix creator FAQ", "url": "https://incubrix.com/faq", "context": "Official technical FAQ and knowledgebase."},
                {"anchor": "test video processing in IncuBrix Studio", "url": "https://app.incubrix.com", "context": "Verify render speed and resolution free."},
                {"anchor": "reframe 16:9 horizontal videos to vertical 9:16", "url": "https://incubrix.com/guides/reframe-horizontal-video-to-vertical-9-16", "context": "Fix aspect ratio and speaker centering issues."}
            ],
            "P08": [
                {"anchor": "connect your social channels in IncuBrix Studio", "url": "https://app.incubrix.com", "context": "Publish directly to YouTube Shorts, TikTok, and Reels."},
                {"anchor": "IncuBrix pricing and credit tiers", "url": "https://incubrix.com/pricing", "context": "Social publishing features available from Starter plan."},
                {"anchor": "turn long videos into shorts with AI", "url": "https://incubrix.com/guides/turn-long-videos-into-shorts-ai", "context": "Generate clips ready for auto-scheduling."}
            ],
            "P09": [
                {"anchor": "read the IncuBrix Creator Manifesto", "url": "https://incubrix.com/manifesto", "context": "Discover the driving philosophy behind CreatorOps."},
                {"anchor": "about IncuBrix Private Limited", "url": "https://incubrix.com/about", "context": "Learn about our founding mission and team."},
                {"anchor": "experience the CreatorOps Studio live", "url": "https://app.incubrix.com", "context": "Explore the unified CreatorOps software architecture."},
                {"anchor": "AI video repurposing for agencies", "url": "https://incubrix.com/solutions/ai-video-repurposing-for-agencies", "context": "See how agencies implement CreatorOps at scale."}
            ],
            "P10": [
                {"anchor": "explore IncuBrix agency pricing tiers", "url": "https://incubrix.com/pricing", "context": "Check out the Growth ($50/mo), Scale ($100/mo), and Pro ($250/mo) tiers."},
                {"anchor": "start agency trial in IncuBrix Studio", "url": "https://app.incubrix.com", "context": "Create a team workspace with multi-user access."},
                {"anchor": "what is CreatorOps?", "url": "https://incubrix.com/glossary/what-is-creatorops-creator-operating-system", "context": "Integrate end-to-end CreatorOps into your agency pitch."}
            ]
        }
        return link_matrix.get(page_id, [
            {"anchor": "IncuBrix homepage", "url": "https://incubrix.com/", "context": "Learn more about the AI CreatorOps platform."},
            {"anchor": "IncuBrix pricing", "url": "https://incubrix.com/pricing", "context": "Compare plans."}
        ])


if __name__ == "__main__":
    links = InternalLinkManager.get_contextual_links_for_page("P01")
    print(f"Contextual links for P01: {len(links)} links")
    for l in links:
        print(f" - [{l['anchor']}]({l['url']}) : {l['context']}")
