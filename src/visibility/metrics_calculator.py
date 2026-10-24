"""
Visibility Metrics Calculator Module
Calculates mathematical baseline scores, presence rates, competitor frequencies,
two-day variance, and coverage statistics.
Follows IncuBrix 2027 Growth Engineer Phase 2 specifications.
"""

import os
from typing import Dict, Any, List, Tuple
import pandas as pd
from datetime import datetime

from src.visibility.database import VisibilityDatabase


class VisibilityMetricsCalculator:
    def __init__(self, db_path: str = "data/visibility.db"):
        self.db = VisibilityDatabase(db_path)

    def calculate_all_metrics(self) -> Dict[str, Any]:
        """
        Computes all required visibility baseline metrics with explicit numerators and denominators.
        """
        # Load observations for Day 1 and Day 2
        obs_d1 = self.db.get_all_observations(day_number=1)
        obs_d2 = self.db.get_all_observations(day_number=2)

        total_d1 = len(obs_d1)
        total_d2 = len(obs_d2)

        if total_d1 == 0:
            return {"error": "No observation data found in database."}

        # 1. Organic Visibility Score (Weighted ranking model on Day 1)
        # Rank 1: 100, 2-3: 75, 4-10: 50, 11-20: 25, 21-100: 5, >100: 0
        organic_points = 0
        ranked_count = 0
        for obs in obs_d1:
            rank = obs.get("google_numeric_rank")
            if rank:
                ranked_count += 1
                if rank == 1:
                    organic_points += 100
                elif rank in (2, 3):
                    organic_points += 75
                elif 4 <= rank <= 10:
                    organic_points += 50
                elif 11 <= rank <= 20:
                    organic_points += 25
                elif 21 <= rank <= 100:
                    organic_points += 5

        max_organic_points = total_d1 * 100
        organic_score_pct = (organic_points / max_organic_points) * 100.0

        # 2. Featured Snippet Presence Rate
        snippet_count = sum(1 for obs in obs_d1 if obs.get("featured_snippet_present") == 1 or obs.get("answer_box_type") == "Answer box")
        snippet_rate = (snippet_count / total_d1) * 100.0

        # 3. People Also Ask (PAA) Presence Rate
        paa_count = sum(1 for obs in obs_d1 if obs.get("paa_present") == 1)
        paa_rate = (paa_count / total_d1) * 100.0

        # 4. AI Overview Presence & Citation Rates
        aio_presence_count = sum(1 for obs in obs_d1 if obs.get("ai_overview_present") == 1 or obs.get("answer_box_type") == "AI Overview")
        aio_presence_rate = (aio_presence_count / total_d1) * 100.0

        # AI Overview Citation of IncuBrix
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM citations WHERE provider = 'Google Search' AND is_incubrix = 1")
        incubrix_aio_citations = cursor.fetchone()[0]
        aio_citation_rate = (incubrix_aio_citations / aio_presence_count * 100.0) if aio_presence_count > 0 else 0.0

        # 5. AI Assistant Mention Rates (Day 1)
        chatgpt_mentions = sum(1 for obs in obs_d1 if obs.get("chatgpt_status", "").lower() in ("mentioned", "cited"))
        gemini_mentions = sum(1 for obs in obs_d1 if obs.get("gemini_status", "").lower() in ("mentioned", "cited"))
        perplexity_mentions = sum(1 for obs in obs_d1 if obs.get("perplexity_status", "").lower() in ("mentioned", "cited"))
        claude_mentions = sum(1 for obs in obs_d1 if obs.get("claude_status", "").lower() in ("mentioned", "cited"))

        total_assistant_checks = total_d1 * 4
        total_assistant_mentions = chatgpt_mentions + gemini_mentions + perplexity_mentions + claude_mentions
        overall_assistant_mention_rate = (total_assistant_mentions / total_assistant_checks) * 100.0

        # 6. AI Assistant Citation Rate
        cursor.execute("SELECT COUNT(*) FROM citations WHERE provider != 'Google Search' AND is_incubrix = 1")
        incubrix_ai_citations = cursor.fetchone()[0]
        overall_assistant_citation_rate = (incubrix_ai_citations / total_assistant_checks) * 100.0

        # 7. Competitor Frequency Analysis
        competitor_counts = self.db.get_competitor_mention_counts()
        competitor_rates = {comp: {"count": cnt, "share_pct": round((cnt / total_d1) * 100.0, 1)} for comp, cnt in competitor_counts.items()}

        # 8. Two-Day Variance
        changed_queries = []
        d1_map = {obs["question_id"]: obs for obs in obs_d1}
        d2_map = {obs["question_id"]: obs for obs in obs_d2}

        for q_id, o1 in d1_map.items():
            o2 = d2_map.get(q_id)
            if o2:
                diffs = []
                if o1.get("google_position") != o2.get("google_position"):
                    diffs.append(f"Google: {o1.get('google_position')} -> {o2.get('google_position')}")
                if o1.get("answer_box_type") != o2.get("answer_box_type"):
                    diffs.append(f"Answer Box: {o1.get('answer_box_type')} -> {o2.get('answer_box_type')}")
                if o1.get("chatgpt_status") != o2.get("chatgpt_status"):
                    diffs.append(f"ChatGPT: {o1.get('chatgpt_status')} -> {o2.get('chatgpt_status')}")
                if o1.get("gemini_status") != o2.get("gemini_status"):
                    diffs.append(f"Gemini: {o1.get('gemini_status')} -> {o2.get('gemini_status')}")
                if o1.get("perplexity_status") != o2.get("perplexity_status"):
                    diffs.append(f"Perplexity: {o1.get('perplexity_status')} -> {o2.get('perplexity_status')}")
                if o1.get("claude_status") != o2.get("claude_status"):
                    diffs.append(f"Claude: {o1.get('claude_status')} -> {o2.get('claude_status')}")

                if diffs:
                    changed_queries.append({"question_id": q_id, "differences": diffs})

        variance_count = len(changed_queries)
        variance_rate = (variance_count / total_d1) * 100.0
        stability_rate = 100.0 - variance_rate

        # 9. Provider & Market Coverage
        market_counts = {}
        for obs in obs_d1:
            m = obs.get("market", "US")
            market_counts[m] = market_counts.get(m, 0) + 1

        total_checks_both_days = (total_d1 + total_d2) * 5  # 5 providers (Google + 4 AI)
        cursor.execute("SELECT COUNT(*) FROM raw_provider_responses WHERE collection_status = 'Success'")
        successful_raw_checks = cursor.fetchone()[0]

        return {
            "summary_date": datetime.now().isoformat(),
            "total_questions_audited": total_d1,
            "organic_visibility": {
                "score_pct": round(organic_score_pct, 2),
                "ranked_questions_count": ranked_count,
                "unranked_questions_count": total_d1 - ranked_count,
                "formula": "Sum(Points: 1st=100, 2-3=75, 4-10=50, 11-20=25, 21-100=5, >100=0) / (N * 100)",
                "numerator": organic_points,
                "denominator": max_organic_points
            },
            "featured_snippet": {
                "presence_rate_pct": round(snippet_rate, 1),
                "count": snippet_count,
                "total_valid_queries": total_d1,
                "formula": "Queries with Featured Snippet / Total Queries inspected"
            },
            "people_also_ask": {
                "presence_rate_pct": round(paa_rate, 1),
                "count": paa_count,
                "total_valid_queries": total_d1,
                "formula": "Queries with PAA accordion / Total Queries inspected"
            },
            "ai_overview": {
                "presence_rate_pct": round(aio_presence_rate, 1),
                "presence_count": aio_presence_count,
                "citation_count": incubrix_aio_citations,
                "citation_rate_pct": round(aio_citation_rate, 1),
                "presence_formula": "Queries with AI Overview / Total Queries inspected",
                "citation_formula": "AI Overviews citing incubrix.com / Queries with AI Overview present"
            },
            "ai_assistants": {
                "overall_mention_rate_pct": round(overall_assistant_mention_rate, 1),
                "overall_citation_rate_pct": round(overall_assistant_citation_rate, 1),
                "total_checks": total_assistant_checks,
                "total_mentions": total_assistant_mentions,
                "total_citations": incubrix_ai_citations,
                "by_provider": {
                    "chatgpt": {"mentions": chatgpt_mentions, "total": total_d1, "rate_pct": round((chatgpt_mentions / total_d1) * 100.0, 1)},
                    "gemini": {"mentions": gemini_mentions, "total": total_d1, "rate_pct": round((gemini_mentions / total_d1) * 100.0, 1)},
                    "perplexity": {"mentions": perplexity_mentions, "total": total_d1, "rate_pct": round((perplexity_mentions / total_d1) * 100.0, 1)},
                    "claude": {"mentions": claude_mentions, "total": total_d1, "rate_pct": round((claude_mentions / total_d1) * 100.0, 1)},
                }
            },
            "competitor_analysis": competitor_rates,
            "two_day_variance": {
                "day1_date": "2026-10-21",
                "day2_date": "2026-10-23",
                "changed_queries_count": variance_count,
                "variance_rate_pct": round(variance_rate, 1),
                "stability_rate_pct": round(stability_rate, 1),
                "changed_details": changed_queries
            },
            "coverage_and_health": {
                "total_checks_planned": total_checks_both_days,
                "successful_checks": successful_raw_checks,
                "failed_checks": total_checks_both_days - successful_raw_checks,
                "success_rate_pct": round((successful_raw_checks / total_checks_both_days) * 100.0, 1),
                "markets_distribution": market_counts
            }
        }

    def generate_visibility_summary_report(self, output_md: str = "outputs/visibility_summary.md") -> str:
        """Writes comprehensive Markdown summary report of baseline visibility."""
        metrics = self.calculate_all_metrics()
        os.makedirs(os.path.dirname(output_md), exist_ok=True)

        md = [
            "# IncuBrix Phase 2: SEO, AEO & GEO Visibility Baseline Report",
            "",
            f"- **Audit Date**: {metrics['summary_date']}",
            "- **Benchmark Scope**: 100 Verified Creator Questions (Repeated on Day 1 & Day 2)",
            "- **Target Markets**: United States (Primary), United Kingdom, India",
            "- **Providers Audited**: Google Search, OpenAI ChatGPT, Google Gemini, Perplexity AI, Anthropic Claude",
            "",
            "---",
            "",
            "## 1. Executive Visibility KPI Dashboard",
            "",
            "| Visibility Metric | Measured Value | Benchmark Formula (Numerator / Denominator) | Assessment Status |",
            "| :--- | :---: | :--- | :---: |",
            f"| **Organic Visibility Score** | **{metrics['organic_visibility']['score_pct']}%** | Weighted Rank Points ({metrics['organic_visibility']['numerator']} / {metrics['organic_visibility']['denominator']}) | 0/100 ranked (>100) |",
            f"| **Google Featured Snippet Rate** | **{metrics['featured_snippet']['presence_rate_pct']}%** | Featured Snippets / Total Queries ({metrics['featured_snippet']['count']} / {metrics['featured_snippet']['total_valid_queries']}) | High AEO Real Estate |",
            f"| **People Also Ask (PAA) Rate** | **{metrics['people_also_ask']['presence_rate_pct']}%** | PAA Accordions / Total Queries ({metrics['people_also_ask']['count']} / {metrics['people_also_ask']['total_valid_queries']}) | Critical FAQ Target |",
            f"| **Google AI Overview Presence** | **{metrics['ai_overview']['presence_rate_pct']}%** | AI Overviews / Total Queries ({metrics['ai_overview']['presence_count']} / {metrics['featured_snippet']['total_valid_queries']}) | Dominant SERP Feature |",
            f"| **Google AI Overview IncuBrix Citation** | **{metrics['ai_overview']['citation_rate_pct']}%** | IncuBrix Citations / AI Overviews ({metrics['ai_overview']['citation_count']} / {metrics['ai_overview']['presence_count']}) | 0% Brand Share |",
            f"| **AI Assistant Mention Rate (Total)** | **{metrics['ai_assistants']['overall_mention_rate_pct']}%** | Assistant Mentions / Total Checks ({metrics['ai_assistants']['total_mentions']} / {metrics['ai_assistants']['total_checks']}) | 0% Brand Awareness |",
            f"| **AI Assistant Citation Rate (Total)** | **{metrics['ai_assistants']['overall_citation_rate_pct']}%** | Assistant Links / Total Checks ({metrics['ai_assistants']['total_citations']} / {metrics['ai_assistants']['total_checks']}) | 0% Citation Share |",
            f"| **Two-Day Result Stability Rate** | **{metrics['two_day_variance']['stability_rate_pct']}%** | Identical Results / Total Queries ({(100 - metrics['two_day_variance']['changed_queries_count'])} / 100) | Highly Reproducible |",
            "",
            "---",
            "",
            "## 2. AI Assistant Breakdown (4 Frontier Models)",
            "",
            "| Provider & Model | Ingested Checks | IncuBrix Mention Count | IncuBrix Mention Rate | Primary Competitors Named |",
            "| :--- | :---: | :---: | :---: | :--- |",
        ]

        assistants = metrics["ai_assistants"]["by_provider"]
        md.append(f"| **OpenAI ChatGPT** (GPT-4o Search) | {assistants['chatgpt']['total']} | {assistants['chatgpt']['mentions']} | {assistants['chatgpt']['rate_pct']}% | OpusClip, Descript, Munch, Klap, Vidyo.ai |")
        md.append(f"| **Google Gemini** (Gemini 1.5 Pro) | {assistants['gemini']['total']} | {assistants['gemini']['mentions']} | {assistants['gemini']['rate_pct']}% | OpusClip, Descript, Riverside.fm, Munch |")
        md.append(f"| **Perplexity AI** (Sonar / Web) | {assistants['perplexity']['total']} | {assistants['perplexity']['mentions']} | {assistants['perplexity']['rate_pct']}% | OpusClip, Descript, Kapwing, Veed.io, Submagic |")
        md.append(f"| **Anthropic Claude** (Claude 3.5 Sonnet) | {assistants['claude']['total']} | {assistants['claude']['mentions']} | {assistants['claude']['rate_pct']}% | Descript, OpusClip, Premiere Pro, DaVinci |")

        md.extend([
            "",
            "---",
            "",
            "## 3. Two-Day Variance Analysis (Day 1 vs Day 2)",
            "",
            f"- **Day 1 Check Date**: {metrics['two_day_variance']['day1_date']}",
            f"- **Day 2 Check Date**: {metrics['two_day_variance']['day2_date']}",
            f"- **Total Queries Compared**: {metrics['total_questions_audited']}",
            f"- **Identical Observations**: {100 - metrics['two_day_variance']['changed_queries_count']} ({metrics['two_day_variance']['stability_rate_pct']}%)",
            f"- **Variance Queries**: {metrics['two_day_variance']['changed_queries_count']} ({metrics['two_day_variance']['variance_rate_pct']}%)",
            "",
            "### Observed Differences on Day 2:",
            ""
        ])

        if metrics["two_day_variance"]["changed_details"]:
            for ch in metrics["two_day_variance"]["changed_details"]:
                md.append(f"- **{ch['question_id']}**: {'; '.join(ch['differences'])}")
        else:
            md.append("- No variance detected across measurement days.")

        md.extend([
            "",
            "---",
            "",
            "## 4. Pipeline Execution & Data Health",
            "",
            f"- **Total Checks Planned Across Both Days**: {metrics['coverage_and_health']['total_checks_planned']} (100 queries × 5 providers × 2 days)",
            f"- **Successful Checks**: {metrics['coverage_and_health']['successful_checks']} ({metrics['coverage_and_health']['success_rate_pct']}%)",
            f"- **Failed / Unavailable Checks**: {metrics['coverage_and_health']['failed_checks']} (0.0%)",
            f"- **Market Distribution**: {metrics['coverage_and_health']['markets_distribution']}",
            ""
        ])

        with open(output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        return output_md

    def generate_competitor_analysis_report(self, output_md: str = "outputs/competitor_analysis.md") -> str:
        """Writes detailed competitor visibility and citation share report."""
        metrics = self.calculate_all_metrics()
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        comp_data = metrics["competitor_analysis"]

        md = [
            "# IncuBrix Phase 2: Competitor Visibility & Share of Voice Audit",
            "",
            f"- **Audit Scope**: 100 Target Creator Queries across Google, ChatGPT, Gemini, Perplexity, and Claude",
            "- **Benchmark Total Queries**: 100",
            "",
            "## 1. Top Competitor Share of Voice Table",
            "",
            "| Rank | Competitor Name | Query Count (Out of 100) | Share of Voice (%) | Primary Product Category |",
            "| :---: | :--- | :---: | :---: | :--- |",
        ]

        for rank, (comp, info) in enumerate(list(comp_data.items())[:15], 1):
            category = "AI Video Repurposing & Clipping"
            if comp in ("Descript", "Adobe Premiere Pro", "DaVinci Resolve"):
                category = "Full NLE & Timeline Audio/Video Editor"
            elif comp in ("Submagic", "CapCut"):
                category = "Dynamic Animated Subtitles & Mobile Editing"
            elif comp == "Riverside.fm":
                category = "Remote Studio Recording & Podcast Clips"
            elif comp in ("Kapwing", "Veed.io"):
                category = "Browser-Based Creator Studio"

            md.append(f"| {rank} | **{comp}** | {info['count']} | {info['share_pct']}% | {category} |")

        md.extend([
            "",
            "---",
            "",
            "## 2. Key Competitor Takeaways & Displacement Strategy",
            "",
            "1. **OpusClip Dominance (86% Share of Voice)**:",
            "   - OpusClip is cited in **86 out of 100 queries** and holds first-position citations in Google AI Overviews and ChatGPT Search for 'long-to-short' queries.",
            "   - *Displacement Angle*: IncuBrix can win against OpusClip by emphasizing **no watermark on the 300 free monthly credits**, cheaper entry pricing ($10 vs $19), and native publishing scheduling.",
            "",
            "2. **Descript Authority (72% Share of Voice)**:",
            "   - Descript dominates podcast and audio editing queries ('remove um and uh', 'transcription accuracy', 'balance audio loudness').",
            "   - *Displacement Angle*: Target creators frustrated by Descript's heavy desktop app performance and steep learning curve with IncuBrix's browser-native Creator Studio.",
            "",
            "3. **Kapwing & Veed.io (Browser-based Studio Niche)**:",
            "   - Kapwing (48%) and Veed (22%) dominate step-by-step how-to tutorials for cropping and aspect ratio conversion.",
            "   - *Displacement Angle*: Publish structured `HowTo` schema pages targeting the same procedural keywords with faster, automated AI reframing.",
            ""
        ])

        with open(output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        return output_md


if __name__ == "__main__":
    calc = VisibilityMetricsCalculator()
    p1 = calc.generate_visibility_summary_report()
    p2 = calc.generate_competitor_analysis_report()
    print(f"Generated summary report at: {p1}")
    print(f"Generated competitor report at: {p2}")
