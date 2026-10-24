"""
IncuBrix Automated Visibility Engine: Content Brief Generator (Phase 6)
Generates structured editorial content briefs for any given question ID or text,
reusing Phase 4 templates and verified IncuBrix product specifications.
"""

import os
import sqlite3
from typing import Dict, Any, Optional, List
from src.engine.database import EngineDatabase
from src.content.fact_checker import FactChecker
from src.content.internal_links import InternalLinkManager


class ContentBriefGenerator:
    """Creates structured, fact-grounded content briefs for any creator question."""

    def __init__(self, db: Optional[EngineDatabase] = None):
        self.db = db or EngineDatabase()
        self.verified_specs = FactChecker.get_verified_specs()

    def generate_brief_for_question(self, question_id: str, output_dir: str = "outputs/briefs") -> Dict[str, Any]:
        """Generates a structured editorial brief for a given question ID."""
        os.makedirs(output_dir, exist_ok=True)
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE question_id = ?;", (question_id.upper(),))
        row = cursor.fetchone()

        if not row:
            raise KeyError(f"Question ID '{question_id}' not found in database.")

        q_dict = dict(row)
        q_text = q_dict["question_text"]
        cat = q_dict["category"]
        intent = q_dict["search_intent"] or "Informational"
        audience = q_dict["target_audience"] or "Video creators, podcasters, and media editors"

        # Generate slug and title
        clean_slug = q_text.lower().replace("?", "").replace("'", "").replace("\"", "")
        clean_slug = "-".join([w for w in clean_slug.split() if len(w) > 2])[:50]
        proposed_title = f"{q_text.rstrip('?')} (Complete Guide) | IncuBrix"

        # Query related questions from same category
        cursor.execute("""
            SELECT question_id, question_text FROM questions 
            WHERE category = ? AND question_id != ? 
            LIMIT 3;
        """, (cat, question_id.upper()))
        related = [f"{r['question_id']}: {r['question_text']}" for r in cursor.fetchall()]

        # Contextual internal links
        int_links = InternalLinkManager.get_contextual_links_for_page("P01")

        # Assembled Brief Dictionary
        brief = {
            "question_id": question_id.upper(),
            "primary_question": q_text,
            "category": cat,
            "search_intent": intent,
            "target_audience": audience,
            "proposed_title": proposed_title,
            "proposed_slug": f"/{cat.lower().replace(' ', '-')}/{clean_slug}",
            "related_questions": related,
            "direct_answer_recommendation": (
                f"Answer '{q_text}' directly in the first two sentences. State the exact software approach, "
                f"estimated processing rate (~14 credits/min in IncuBrix), and key feature benefit without fluff."
            ),
            "suggested_outline": [
                f"H1: {proposed_title}",
                "H2: 1. Core Direct Answer & Workflow Summary (AEO Focus)",
                "H2: 2. Why Creators Struggle with This Workflow (Technical Bottlenecks)",
                "H2: 3. Step-by-Step Practical Implementation Guide",
                "   H3: Step 1: Media Ingestion & Speech Diarization",
                "   H3: Step 2: Computer Vision 9:16 Framing & Active Speaker Tracking",
                "   H3: Step 3: Kinetic Subtitles & Emoji Syncing",
                "H2: 4. Production Economics: Credit Consumption & Time Savings",
                "H2: 5. Common Troubleshooting & FAQs",
                "H2: 6. Recommended Next Steps & Tool Trial"
            ],
            "verified_product_anchors": {
                "product_name": self.verified_specs["product_name"],
                "positioning": self.verified_specs["positioning"],
                "credit_consumption": "~14 credits per 1 minute of processed video",
                "free_tier": "Free plan includes 300 credits with zero credit card required",
                "app_url": self.verified_specs["app_url"]
            },
            "internal_link_opportunities": int_links,
            "suggested_structured_data": [
                "Article / BlogPosting",
                "BreadcrumbList",
                "HowTo (if step-by-step) or FAQPage (if Q&A format)"
            ],
            "fact_checking_requirements": [
                "Verify all competitor capabilities against published 2026 documentation",
                "Do not state unsupported claims (e.g. 'guaranteed virality')",
                "Ensure all statistics cite traceable external URLs",
                "Confirm credit economics match IncuBrix standard (~14 credits/min)"
            ]
        }

        # Write markdown brief
        md_path = os.path.join(output_dir, f"brief_{question_id.lower()}.md")
        md_lines = [
            f"# Editorial Content Brief: {question_id.upper()}",
            "",
            f"- **Target Question**: `{brief['primary_question']}`",
            f"- **Category**: `{brief['category']}`",
            f"- **Search Intent**: `{brief['search_intent']}`",
            f"- **Target Audience**: {brief['target_audience']}",
            f"- **Proposed Title**: `{brief['proposed_title']}`",
            f"- **Proposed Slug**: `{brief['proposed_slug']}`",
            "",
            "---",
            "",
            "## 1. Direct-Answer Strategy (AEO & AI Overview Target)",
            "",
            f"> **Constraint**: {brief['direct_answer_recommendation']}",
            "",
            "---",
            "",
            "## 2. Related Questions from Research",
            ""
        ]
        for r in brief["related_questions"]:
            md_lines.append(f"- `{r}`")

        md_lines.extend([
            "",
            "---",
            "",
            "## 3. Recommended Heading Outline",
            ""
        ])
        for h in brief["suggested_outline"]:
            md_lines.append(f"- {h}")

        md_lines.extend([
            "",
            "---",
            "",
            "## 4. Verified IncuBrix Anchors to Feature",
            "",
            f"- **Positioning**: {brief['verified_product_anchors']['positioning']}",
            f"- **Credit Consumption**: {brief['verified_product_anchors']['credit_consumption']}",
            f"- **Free Tier**: {brief['verified_product_anchors']['free_tier']}",
            f"- **App Link**: [{brief['verified_product_anchors']['app_url']}]({brief['verified_product_anchors']['app_url']})",
            "",
            "---",
            "",
            "## 5. Contextual Internal Links",
            ""
        ])
        for l in brief["internal_link_opportunities"]:
            md_lines.append(f"- [{l['anchor']}]({l['url']}) — *{l['context']}*")

        md_lines.extend([
            "",
            "---",
            "",
            "## 6. Required Structured Data & Fact-Checking",
            "",
            "**Structured Data Schemas:**",
            "- Article",
            "- BreadcrumbList",
            "- HowTo / FAQPage",
            "",
            "**Fact-Checking Checklist:**"
        ])
        for fc in brief["fact_checking_requirements"]:
            md_lines.append(f"- [ ] {fc}")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        brief["markdown_path"] = md_path
        return brief


if __name__ == "__main__":
    cbg = ContentBriefGenerator()
    brief = cbg.generate_brief_for_question("Q021")
    print(f"Content Brief generated for {brief['question_id']}:")
    print(f"Title: {brief['proposed_title']}")
    print(f"Saved to: {brief['markdown_path']}")
    cbg.db.close()
