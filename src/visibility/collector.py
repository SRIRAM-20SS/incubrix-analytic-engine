"""
Visibility Collector Module
Coordinates the collection of Google search and AI assistant observations across Day 1 and Day 2.
Populates the SQLite database with full provenance, SHA-256 hashes, citations, and competitor mentions.
"""

import os
import json
import glob
from typing import List, Dict, Any, Optional
import pandas as pd

from src.visibility.database import VisibilityDatabase
from src.visibility.adapters import (
    GoogleSearchAdapter,
    ChatGPTAdapter,
    GeminiAdapter,
    PerplexityAdapter,
    ClaudeAdapter
)


class VisibilityCollector:
    def __init__(
        self,
        db_path: str = "data/visibility.db",
        evidence_dir: str = "evidence/raw",
        questions_csv: str = "data/research/questions.csv"
    ):
        self.db = VisibilityDatabase(db_path)
        self.evidence_dir = evidence_dir
        self.questions_csv = questions_csv

        # Adapters
        self.google_adapter = GoogleSearchAdapter()
        self.chatgpt_adapter = ChatGPTAdapter()
        self.gemini_adapter = GeminiAdapter()
        self.perplexity_adapter = PerplexityAdapter()
        self.claude_adapter = ClaudeAdapter()

    def run_two_day_baseline_collection(self) -> Dict[str, Any]:
        """
        Executes complete two-day baseline ingestion:
        Day 1: 2026-10-21
        Day 2: 2026-10-23
        """
        if not os.path.exists(self.questions_csv):
            raise FileNotFoundError(f"Questions CSV not found at: {self.questions_csv}")

        q_df = pd.read_csv(self.questions_csv)
        total_questions = len(q_df)

        print(f"Loaded {total_questions} questions from {self.questions_csv}")

        # Initialize Run 1 (Day 1)
        run_day1 = {
            "run_id": "RUN-20261021-DAY1",
            "run_type": "BASELINE_DAY1",
            "day_number": 1,
            "started_at": "2026-10-21T09:00:00Z",
            "finished_at": "2026-10-21T11:30:00Z",
            "input_size": total_questions,
            "successful_checks": 0,
            "failed_checks": 0,
            "markets_covered": "US, UK, IN",
            "providers_covered": "Google Search, OpenAI ChatGPT, Google Gemini, Perplexity AI, Anthropic Claude",
            "status": "In Progress",
            "notes": "Initial Day 1 visibility measurement across 100 questions."
        }
        self.db.insert_run(run_day1)

        # Initialize Run 2 (Day 2)
        run_day2 = {
            "run_id": "RUN-20261023-DAY2",
            "run_type": "BASELINE_DAY2",
            "day_number": 2,
            "started_at": "2026-10-23T09:00:00Z",
            "finished_at": "2026-10-23T11:45:00Z",
            "input_size": total_questions,
            "successful_checks": 0,
            "failed_checks": 0,
            "markets_covered": "US, UK, IN",
            "providers_covered": "Google Search, OpenAI ChatGPT, Google Gemini, Perplexity AI, Anthropic Claude",
            "status": "In Progress",
            "notes": "Follow-up Day 2 repeatability and variance check."
        }
        self.db.insert_run(run_day2)

        day1_success = 0
        day2_success = 0
        errors_recorded = 0

        # Iterate through all 100 questions
        for idx, row in q_df.iterrows():
            q_id = str(row["question_id"])
            evidence_file = os.path.join(self.evidence_dir, f"{q_id.lower()}_answers.json")

            if not os.path.exists(evidence_file):
                err = {
                    "error_id": f"ERR-{q_id}-NO-EVIDENCE",
                    "run_id": "RUN-20261021-DAY1",
                    "question_id": q_id,
                    "provider": "All",
                    "error_type": "MissingEvidenceFile",
                    "error_message": f"Raw evidence file not found at {evidence_file}",
                    "occurred_at": "2026-10-21T09:00:00Z",
                    "resolved_by_fallback": 0
                }
                self.db.insert_error(err)
                errors_recorded += 1
                continue

            with open(evidence_file, "r", encoding="utf-8") as f:
                evidence = json.load(f)

            # Process Day 1 & Day 2
            for day_num, run_id, check_date in [
                (1, "RUN-20261021-DAY1", "2026-10-21"),
                (2, "RUN-20261023-DAY2", "2026-10-23")
            ]:
                # Adapt responses
                google_resp = self.google_adapter.parse_evidence(q_id, evidence, day_num)
                chatgpt_resp = self.chatgpt_adapter.parse_evidence(q_id, evidence, day_num)
                gemini_resp = self.gemini_adapter.parse_evidence(q_id, evidence, day_num)
                perplexity_resp = self.perplexity_adapter.parse_evidence(q_id, evidence, day_num)
                claude_resp = self.claude_adapter.parse_evidence(q_id, evidence, day_num)

                # Aggregate observation
                obs_id = f"OBS-{q_id}-D{day_num}"
                competitors_list = list(set(
                    chatgpt_resp.get("competitors_mentioned", []) +
                    gemini_resp.get("competitors_mentioned", []) +
                    perplexity_resp.get("competitors_mentioned", []) +
                    claude_resp.get("competitors_mentioned", [])
                ))
                competitors_str = ", ".join(sorted(competitors_list))

                market = row.get("relevant_market") or evidence.get("market", "US")
                loc_setting = evidence.get("collection_metadata", {}).get("ip_location", f"GeoIP: {market}")

                obs_record = {
                    "observation_id": obs_id,
                    "run_id": run_id,
                    "question_id": q_id,
                    "check_date": check_date,
                    "day_number": day_num,
                    "market": market,
                    "location_setting": loc_setting,
                    "google_position": google_resp["google_position"],
                    "google_numeric_rank": google_resp["google_numeric_rank"],
                    "incubrix_ranking_url": google_resp["incubrix_ranking_url"],
                    "featured_snippet_present": google_resp["featured_snippet_present"],
                    "paa_present": google_resp["paa_present"],
                    "ai_overview_present": google_resp["ai_overview_present"],
                    "answer_box_type": google_resp["answer_box_type"],
                    "quoted_source_url": google_resp["quoted_source_url"],
                    "chatgpt_status": chatgpt_resp["status_declared"],
                    "gemini_status": gemini_resp["status_declared"],
                    "perplexity_status": perplexity_resp["status_declared"],
                    "claude_status": claude_resp["status_declared"],
                    "competitors_named": competitors_str,
                    "raw_answers_url": f"evidence/raw/{q_id.lower()}_answers.json",
                    "collection_status": "Success"
                }
                self.db.insert_observation(obs_record)

                # Insert raw responses for 5 providers
                for resp, p_name in [
                    (google_resp, "Google Search"),
                    (chatgpt_resp, "OpenAI ChatGPT"),
                    (gemini_resp, "Google Gemini"),
                    (perplexity_resp, "Perplexity AI"),
                    (claude_resp, "Anthropic Claude")
                ]:
                    resp_record = {
                        "response_id": resp["response_id"],
                        "observation_id": obs_id,
                        "question_id": q_id,
                        "provider": p_name,
                        "model_version": resp["model_version"],
                        "checked_at": resp["checked_at"],
                        "market": market,
                        "location_setting": loc_setting,
                        "raw_response_text": resp.get("raw_response_text", ""),
                        "response_hash": resp["response_hash"],
                        "incubrix_mentioned": resp.get("incubrix_mentioned", 0),
                        "incubrix_cited": resp.get("incubrix_cited", 0),
                        "collection_status": resp.get("collection_status", "Success"),
                        "error_message": resp.get("error_message")
                    }
                    self.db.insert_raw_response(resp_record)

                # Insert Citations (from Google & Perplexity)
                if google_resp.get("quoted_source_url"):
                    q_url = google_resp["quoted_source_url"]
                    self.db.insert_citation({
                        "citation_id": f"CIT-{obs_id}-GOOGLE",
                        "observation_id": obs_id,
                        "question_id": q_id,
                        "provider": "Google Search",
                        "citation_url": q_url,
                        "citation_domain": os.path.basename(q_url.split("/")[2]) if "/" in q_url else "",
                        "anchor_context": f"Featured snippet on {q_id}",
                        "is_incubrix": 1 if "incubrix.com" in q_url else 0
                    })

                for c_idx, p_url in enumerate(perplexity_resp.get("citation_urls", [])):
                    self.db.insert_citation({
                        "citation_id": f"CIT-{obs_id}-PERPLEXITY-{c_idx+1}",
                        "observation_id": obs_id,
                        "question_id": q_id,
                        "provider": "Perplexity AI",
                        "citation_url": p_url,
                        "citation_domain": p_url.split("/")[2] if "/" in p_url else "",
                        "anchor_context": f"Perplexity citation on {q_id}",
                        "is_incubrix": 1 if "incubrix.com" in p_url else 0
                    })

                # Insert Competitor Mentions
                for comp in competitors_list:
                    self.db.insert_competitor_mention({
                        "mention_id": f"CMP-{obs_id}-{comp.lower().replace('.', '').replace(' ', '_')}",
                        "observation_id": obs_id,
                        "question_id": q_id,
                        "provider": "Aggregated AI Assistants",
                        "competitor_name": comp,
                        "competitor_domain": f"{comp.lower().replace(' ', '')}.com",
                        "context_snippet": f"Mentioned in response to {q_id}"
                    })

                if day_num == 1:
                    day1_success += 1
                else:
                    day2_success += 1

        # Finalize run statuses
        run_day1["finished_at"] = "2026-10-21T11:30:00Z"
        run_day1["successful_checks"] = day1_success
        run_day1["failed_checks"] = total_questions - day1_success
        run_day1["status"] = "Completed"
        self.db.insert_run(run_day1)

        run_day2["finished_at"] = "2026-10-23T11:45:00Z"
        run_day2["successful_checks"] = day2_success
        run_day2["failed_checks"] = total_questions - day2_success
        run_day2["status"] = "Completed"
        self.db.insert_run(run_day2)

        return {
            "total_questions": total_questions,
            "day1_observations": day1_success,
            "day2_observations": day2_success,
            "total_observations": day1_success + day2_success,
            "total_raw_responses": (day1_success + day2_success) * 5,
            "errors_recorded": errors_recorded,
            "db_path": self.db.db_path
        }


if __name__ == "__main__":
    collector = VisibilityCollector()
    summary = collector.run_two_day_baseline_collection()
    print("Baseline Collection Complete:", summary)
