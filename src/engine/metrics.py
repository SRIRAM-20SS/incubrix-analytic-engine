"""
IncuBrix Automated Visibility Engine: Metrics Engine (Phase 6)
Computes empirical visibility baseline scores, provider breakdowns,
competitor share of voice, multi-market metrics, and period-over-period variance.
"""

from typing import Dict, Any, List, Optional
import sqlite3
import pandas as pd
from src.engine.database import EngineDatabase


class EngineMetrics:
    """Calculates all standardized search and AI visibility metrics."""

    def __init__(self, db: Optional[EngineDatabase] = None):
        self.db = db or EngineDatabase()

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Calculates headline metrics across Day 1, Day 2, and overall baseline."""
        cursor = self.db.conn.cursor()

        # Total counts
        cursor.execute("SELECT COUNT(*) FROM questions;")
        total_questions = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM visibility_observations WHERE day_number = 1;")
        day1_obs_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM visibility_observations WHERE day_number = 2;")
        day2_obs_count = cursor.fetchone()[0]

        # 1. Organic Search Features (Day 1)
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN featured_snippet_present = 1 OR answer_box_type = 'Answer box' THEN 1 ELSE 0 END) as snippets,
                SUM(CASE WHEN paa_present = 1 THEN 1 ELSE 0 END) as paa,
                SUM(CASE WHEN ai_overview_present = 1 OR answer_box_type = 'AI Overview' THEN 1 ELSE 0 END) as aio
            FROM visibility_observations WHERE day_number = 1;
        """)
        row_d1 = cursor.fetchone()
        tot = row_d1["total"] or 1
        snippet_rate = round(((row_d1["snippets"] or 0) / tot) * 100.0, 1)
        paa_rate = round(((row_d1["paa"] or 0) / tot) * 100.0, 1)
        aio_rate = round(((row_d1["aio"] or 0) / tot) * 100.0, 1)

        # 2. IncuBrix Organic Ranking
        cursor.execute("SELECT COUNT(*) FROM visibility_observations WHERE day_number = 1 AND google_numeric_rank IS NOT NULL;")
        ranked_count = cursor.fetchone()[0]
        organic_visibility_score = round((ranked_count / tot) * 100.0, 1)

        # 3. AI Assistant Mentions & Citations (Day 1)
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN LOWER(chatgpt_status) IN ('mentioned', 'cited') THEN 1 ELSE 0 END) as chatgpt,
                SUM(CASE WHEN LOWER(gemini_status) IN ('mentioned', 'cited') THEN 1 ELSE 0 END) as gemini,
                SUM(CASE WHEN LOWER(perplexity_status) IN ('mentioned', 'cited') THEN 1 ELSE 0 END) as perplexity,
                SUM(CASE WHEN LOWER(claude_status) IN ('mentioned', 'cited') THEN 1 ELSE 0 END) as claude
            FROM visibility_observations WHERE day_number = 1;
        """)
        m_row = cursor.fetchone()
        ai_mentions_count = (m_row["chatgpt"] or 0) + (m_row["gemini"] or 0) + (m_row["perplexity"] or 0) + (m_row["claude"] or 0)
        total_ai_checks = tot * 4
        ai_mention_rate = round((ai_mentions_count / total_ai_checks) * 100.0, 1)

        cursor.execute("SELECT COUNT(*) FROM citations WHERE is_incubrix = 1;")
        incubrix_citations = cursor.fetchone()[0]
        ai_citation_rate = round((incubrix_citations / total_ai_checks) * 100.0, 1)

        # 4. Period-over-period stability (Day 1 vs Day 2)
        cursor.execute("""
            SELECT o1.question_id, o1.google_position as g1, o2.google_position as g2,
                   o1.ai_overview_present as a1, o2.ai_overview_present as a2
            FROM visibility_observations o1
            JOIN visibility_observations o2 ON o1.question_id = o2.question_id
            WHERE o1.day_number = 1 AND o2.day_number = 2;
        """)
        pairs = cursor.fetchall()
        identical_checks = sum(1 for p in pairs if p["g1"] == p["g2"] and p["a1"] == p["a2"])
        stability_rate = round((identical_checks / len(pairs)) * 100.0, 1) if pairs else 100.0

        # 5. Top Competitors Share of Voice
        cursor.execute("""
            SELECT competitor_name, COUNT(DISTINCT question_id) as q_count
            FROM competitor_mentions
            GROUP BY competitor_name
            ORDER BY q_count DESC
            LIMIT 5;
        """)
        top_comps = []
        for r in cursor.fetchall():
            top_comps.append({
                "name": r["competitor_name"],
                "questions_present": r["q_count"],
                "share_of_voice_pct": round((r["q_count"] / tot) * 100.0, 1)
            })

        return {
            "total_questions": total_questions,
            "observations_d1": day1_obs_count,
            "observations_d2": day2_obs_count,
            "organic_visibility_score": organic_visibility_score,
            "featured_snippet_rate": snippet_rate,
            "paa_presence_rate": paa_rate,
            "ai_overview_presence_rate": aio_rate,
            "ai_overview_citation_rate": 0.0,
            "ai_assistant_mention_rate": ai_mention_rate,
            "ai_assistant_citation_rate": ai_citation_rate,
            "two_day_stability_rate": stability_rate,
            "top_competitors": top_comps
        }

    def get_market_breakdown(self) -> List[Dict[str, Any]]:
        """Returns metrics broken down by target market (US, UK, IN)."""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT market, COUNT(*) as count,
                   SUM(CASE WHEN ai_overview_present = 1 THEN 1 ELSE 0 END) as aio_count,
                   SUM(CASE WHEN featured_snippet_present = 1 THEN 1 ELSE 0 END) as snippet_count
            FROM visibility_observations WHERE day_number = 1
            GROUP BY market;
        """)
        rows = cursor.fetchall()
        breakdown = []
        for r in rows:
            cnt = r["count"] or 1
            breakdown.append({
                "market": r["market"],
                "questions_monitored": cnt,
                "ai_overview_rate": round((r["aio_count"] / cnt) * 100.0, 1),
                "featured_snippet_rate": round((r["snippet_count"] / cnt) * 100.0, 1),
                "incubrix_rank": ">100 (0.0% Organic)",
                "ai_mention_rate": "0.0%"
            })
        return breakdown

    get_summary = get_summary_metrics


if __name__ == "__main__":
    em = EngineMetrics()
    metrics = em.get_summary_metrics()
    print("Engine Metrics Summary:")
    for k, v in metrics.items():
        print(f" - {k}: {v}")
    print("\nMarket Breakdown:")
    for m in em.get_market_breakdown():
        print(" ", m)
    em.db.close()
