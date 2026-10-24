"""
Baseline Exporter Module
Aggregates observation records from the SQLite database into the assessment workbook's
official 02_QUESTIONS schema and exports to visibility.csv.
"""

import os
from typing import Dict, Any, List
import pandas as pd

from src.visibility.database import VisibilityDatabase

WORKBOOK_COLUMNS = [
    "question_id",
    "question",
    "intent",
    "source_type",
    "source_url",
    "market",
    "google_position",
    "answer_box_or_ai_overview",
    "quoted_source_url",
    "chatgpt",
    "gemini",
    "perplexity",
    "claude_or_copilot",
    "competitors_named",
    "check_date_day1",
    "check_date_day2",
    "changed_on_day2",
    "raw_answers_url",
    "priority",
    "notes"
]


def export_visibility_csv(
    db_path: str = "data/visibility.db",
    questions_csv: str = "data/research/questions.csv",
    output_path: str = "data/visibility.csv",
    secondary_output: str = "outputs/visibility.csv"
) -> str:
    """
    Constructs the 100-row workbook-compatible visibility.csv from the SQLite database
    and Phase 1 questions metadata.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if secondary_output:
        os.makedirs(os.path.dirname(secondary_output), exist_ok=True)

    db = VisibilityDatabase(db_path)
    q_df = pd.read_csv(questions_csv)

    # Fetch observations grouped by question_id
    obs_d1 = {row["question_id"]: row for row in db.get_all_observations(day_number=1)}
    obs_d2 = {row["question_id"]: row for row in db.get_all_observations(day_number=2)}

    export_rows: List[Dict[str, Any]] = []

    for idx, q_row in q_df.iterrows():
        q_id = str(q_row["question_id"])
        d1 = obs_d1.get(q_id, {})
        d2 = obs_d2.get(q_id, {})

        # Compute if any metric changed on Day 2
        changed = "No"
        if d1 and d2:
            if (
                d1.get("google_position") != d2.get("google_position") or
                d1.get("answer_box_type") != d2.get("answer_box_type") or
                d1.get("chatgpt_status") != d2.get("chatgpt_status") or
                d1.get("gemini_status") != d2.get("gemini_status") or
                d1.get("perplexity_status") != d2.get("perplexity_status") or
                d1.get("claude_status") != d2.get("claude_status")
            ):
                changed = "Yes"

        # Determine priority based on commercial intent & competitor density
        intent = str(q_row.get("search_intent", "Informational"))
        category = str(q_row.get("category", ""))
        priority = "Medium"
        if intent in ("Commercial", "Comparison") or "Repurposing" in category or "Pricing" in category:
            priority = "High"
        elif "Troubleshooting" in category or "Growth" in category:
            priority = "Medium"
        else:
            priority = "Low"

        row_dict = {
            "question_id": q_id,
            "question": q_row.get("question_text", ""),
            "intent": intent,
            "source_type": q_row.get("source_type", ""),
            "source_url": q_row.get("source_url", ""),
            "market": d1.get("market") or q_row.get("relevant_market", "US"),
            "google_position": d1.get("google_position", ">100"),
            "answer_box_or_ai_overview": d1.get("answer_box_type", "None"),
            "quoted_source_url": d1.get("quoted_source_url") or "",
            "chatgpt": d1.get("chatgpt_status", "Not mentioned"),
            "gemini": d1.get("gemini_status", "Not mentioned"),
            "perplexity": d1.get("perplexity_status", "Not mentioned"),
            "claude_or_copilot": d1.get("claude_status", "Not mentioned"),
            "competitors_named": d1.get("competitors_named", ""),
            "check_date_day1": d1.get("check_date", "2026-10-21"),
            "check_date_day2": d2.get("check_date", "2026-10-23"),
            "changed_on_day2": changed,
            "raw_answers_url": d1.get("raw_answers_url", f"evidence/raw/{q_id.lower()}_answers.json"),
            "priority": priority,
            "notes": q_row.get("notes", "")
        }
        export_rows.append(row_dict)

    df_out = pd.DataFrame(export_rows, columns=WORKBOOK_COLUMNS)
    df_out.to_csv(output_path, index=False)
    if secondary_output:
        df_out.to_csv(secondary_output, index=False)

    return output_path


if __name__ == "__main__":
    path = export_visibility_csv()
    print(f"Exported workbook-compatible visibility.csv to {path}")
