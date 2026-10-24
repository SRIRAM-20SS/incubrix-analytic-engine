"""
IncuBrix Citation Engine: Prioritize Targets (Phase 5)
Implements an objective, multi-criteria scoring algorithm to rank all 30 citation targets.
Criteria: Relevance, Publisher Credibility, Discoverability Evidence, Competitor Density,
and Ethical Feasibility. Does not invent fabricated traffic or DA metrics.
"""

from typing import List, Dict, Any
import pandas as pd
from src.citations.discover_targets import TargetDiscoverer


class TargetPrioritizer:
    """Ranks citation opportunities using a transparent 6-factor framework."""

    @staticmethod
    def calculate_target_score(target: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates reproducible priority score for a target."""
        # 1. Relevance Score (1-5)
        relevance_score = 5 if any(k in target["target_question"].lower() for k in ["turn long videos", "opusclip", "podcast", "reframe"]) else 4

        # 2. Publisher Credibility & Authority (1-5)
        pub = target["publisher_name"].lower()
        if any(p in pub for p in ["g2", "capterra", "pcmag", "techradar", "zapier", "influencer marketing hub"]):
            credibility_score = 5
        elif any(p in pub for p in ["buffer", "social media examiner", "riverside", "vidiq", "econsultancy", "reddit"]):
            credibility_score = 4
        else:
            credibility_score = 3

        # 3. Discoverability & AI Citation Evidence (1-5)
        has_ai = "yes" in target["observed_in_ai_answer"].lower()
        has_google = "yes" in target["observed_in_google"].lower()
        if has_ai and has_google:
            discoverability_score = 5
        elif has_ai:
            discoverability_score = 4
        elif has_google:
            discoverability_score = 3
        else:
            discoverability_score = 2

        # 4. Competitor Density (1-5)
        comps = [c.strip() for c in target["competing_brands_mentioned"].split(",")]
        comp_score = min(5, max(2, len(comps) + 1))

        # 5. Editorial Fit & Ethical Action Feasibility (1-5)
        ptype = target["page_type"].lower()
        if "directory" in ptype or "community" in ptype:
            action_score = 5  # Direct self-claim or community contribution
        elif "best tools" in ptype or "comparison" in ptype:
            action_score = 4  # Editorial pitch with product docs
        else:
            action_score = 3  # Content reference or technical benchmark

        # Total Composite Score (Max 25)
        composite_score = relevance_score + credibility_score + discoverability_score + comp_score + action_score

        # Determine priority category
        if composite_score >= 22:
            calculated_priority = "Critical"
        elif composite_score >= 18:
            calculated_priority = "High"
        else:
            calculated_priority = "Medium"

        return {
            "target_id": target["target_id"],
            "publisher_name": target["publisher_name"],
            "relevance_score": relevance_score,
            "credibility_score": credibility_score,
            "discoverability_score": discoverability_score,
            "competitor_density_score": comp_score,
            "action_feasibility_score": action_score,
            "composite_score": composite_score,
            "calculated_priority": calculated_priority
        }

    @classmethod
    def rank_all_targets(cls) -> List[Dict[str, Any]]:
        targets = TargetDiscoverer.get_all_targets()
        ranked = []
        for t in targets:
            scores = cls.calculate_target_score(t)
            merged = dict(t)
            merged.update(scores)
            ranked.append(merged)

        # Sort by composite score descending
        ranked.sort(key=lambda x: x["composite_score"], reverse=True)
        return ranked


if __name__ == "__main__":
    ranked = TargetPrioritizer.rank_all_targets()
    print(f"Ranked {len(ranked)} targets:")
    for r in ranked[:10]:
        print(f"[{r['target_id']}] Score: {r['composite_score']} | Prio: {r['calculated_priority']} | {r['publisher_name']}: {r['page_title'][:40]}...")
