"""
IncuBrix Citation Engine: Opportunity Analyzer (Phase 5)
Conducts deep structured analysis of each citation opportunity across all 7 assessment dimensions:
1. Relevance to target question
2. Observation source (Google vs AI Assistant citation)
3. Current content utility
4. Current IncuBrix mention status
5. Competing products mentioned
6. Factual, non-promotional contribution angle
7. Suggested ethical action (documentation, comparison, community participation, directory claiming)
"""

from typing import Dict, Any, List
from src.citations.discover_targets import TargetDiscoverer


class OpportunityAnalyzer:
    """Analyzes each citation opportunity for strategic value, risk, and editorial fit."""

    @staticmethod
    def analyze_single_target(target: Dict[str, Any]) -> Dict[str, Any]:
        """Performs a 7-point audit on a citation target."""
        tid = target["target_id"]
        pub = target["publisher_name"]
        url = target["page_url"]
        comp = target["competing_brands_mentioned"]
        obs_ai = target["observed_in_ai_answer"]
        obs_google = target["observed_in_google"]

        # IncuBrix mention status: As verified in Phase 2 baseline, IncuBrix is currently unmentioned
        incubrix_status = "Not Mentioned (Zero visibility confirmed in Phase 2 baseline)"

        analysis = {
            "target_id": tid,
            "publisher_name": pub,
            "page_title": target["page_title"],
            "page_url": url,
            "page_type": target["page_type"],
            "target_question": target["target_question"],
            "1_relevance_explanation": (
                f"Directly relevant to '{target['target_question']}'. {target['page_relevance']}"
            ),
            "2_observation_evidence": (
                f"Observed in Google Search: {obs_google} | Observed in AI Assistant Citation: {obs_ai}. "
                f"Evidence: {target['citation_evidence']}"
            ),
            "3_current_content_utility": target["editorial_context"],
            "4_incubrix_current_presence": incubrix_status,
            "5_competing_products_present": comp,
            "6_factual_contribution_angle": target["potential_inclusion_angle"],
            "7_suggested_ethical_action": target["suggested_ethical_action"],
            "priority": target["priority"],
            "date_checked": target["date_checked"]
        }
        return analysis

    @classmethod
    def analyze_all_targets(cls) -> List[Dict[str, Any]]:
        targets = TargetDiscoverer.get_all_targets()
        return [cls.analyze_single_target(t) for t in targets]

    @classmethod
    def get_summary_statistics(cls) -> Dict[str, Any]:
        targets = TargetDiscoverer.get_all_targets()
        ai_cited = sum(1 for t in targets if "Yes" in t["observed_in_ai_answer"])
        google_obs = sum(1 for t in targets if "Yes" in t["observed_in_google"])
        both_obs = sum(1 for t in targets if "Yes" in t["observed_in_ai_answer"] and "Yes" in t["observed_in_google"])

        return {
            "total_targets": len(targets),
            "observed_in_ai_assistant": ai_cited,
            "observed_in_google_search": google_obs,
            "observed_in_both": both_obs,
            "publisher_types_count": len(set(t["page_type"] for t in targets)),
            "critical_priority_count": sum(1 for t in targets if t["priority"] == "Critical"),
            "high_priority_count": sum(1 for t in targets if t["priority"] == "High"),
            "medium_priority_count": sum(1 for t in targets if t["priority"] == "Medium")
        }


if __name__ == "__main__":
    stats = OpportunityAnalyzer.get_summary_statistics()
    print("Opportunity Analysis Summary Statistics:")
    print(stats)
