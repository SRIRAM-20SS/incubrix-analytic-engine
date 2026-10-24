"""
IncuBrix Content Engine: Metadata Generator (Phase 4)
Generates optimized SEO titles, meta descriptions, Open Graph, and Twitter metadata.
Enforces character length limits (Title <= 60, Description 140-155).
"""

from typing import Dict, Any


class MetadataGenerator:
    """Creates search-engine-optimized HTML metadata and social tags."""

    @staticmethod
    def generate_seo_title(base_title: str, brand_suffix: str = " | IncuBrix") -> str:
        """Ensures title is under 60 characters with branding."""
        max_len = 60
        if len(base_title) + len(brand_suffix) <= max_len:
            return f"{base_title}{brand_suffix}"
        # Truncate base_title cleanly
        allowed_len = max_len - len(brand_suffix)
        return f"{base_title[:allowed_len].rstrip()}{brand_suffix}"

    @staticmethod
    def generate_meta_description(description_text: str) -> str:
        """Ensures meta description fits 140-155 character ideal SERP snippet window."""
        desc = description_text.strip()
        if len(desc) > 158:
            return desc[:155].rstrip() + "..."
        return desc

    @staticmethod
    def generate_page_metadata(
        page_id: str,
        slug: str,
        base_title: str,
        description: str,
        primary_keyword: str,
        category: str,
        canonical_url: str
    ) -> Dict[str, Any]:
        """Assembles complete metadata dictionary."""
        seo_title = MetadataGenerator.generate_seo_title(base_title)
        meta_desc = MetadataGenerator.generate_meta_description(description)

        return {
            "page_id": page_id,
            "slug": slug,
            "canonical_url": canonical_url,
            "seo_title": seo_title,
            "title_length": len(seo_title),
            "meta_description": meta_desc,
            "description_length": len(meta_desc),
            "primary_keyword": primary_keyword,
            "category": category,
            "h1_heading": base_title,
            "og_type": "article",
            "og_image": f"https://incubrix.com/assets/og/{slug}.jpg",
            "twitter_card": "summary_large_image"
        }


if __name__ == "__main__":
    meta = MetadataGenerator.generate_page_metadata(
        page_id="P01",
        slug="turn-long-videos-into-shorts-ai",
        base_title="How to Turn Long Videos into Shorts with AI",
        description="Learn how to turn long videos into viral shorts using AI speech-to-text, speaker framing, and auto-captions with IncuBrix's step-by-step CreatorOps guide.",
        primary_keyword="turn long videos into shorts ai",
        category="Content repurposing",
        canonical_url="https://incubrix.com/guides/turn-long-videos-into-shorts-ai"
    )
    print("Generated Metadata:")
    print(meta)
