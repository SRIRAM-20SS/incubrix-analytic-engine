"""
Visibility Database Module
Manages SQLite persistence for Phase 2 visibility collection runs, observations, raw responses,
citations, competitor mentions, and collection errors.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional
import pandas as pd


class VisibilityDatabase:
    def __init__(self, db_path: str = "data/visibility.db"):
        from src.engine.database import resolve_writable_db_path
        self.db_path = resolve_writable_db_path(db_path)
        if self.db_path != ":memory:" and os.path.dirname(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

    def init_schema(self):
        cursor = self.conn.cursor()

        # 1. Collection Runs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collection_runs (
                run_id TEXT PRIMARY KEY,
                run_type TEXT NOT NULL,
                day_number INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                input_size INTEGER NOT NULL,
                successful_checks INTEGER DEFAULT 0,
                failed_checks INTEGER DEFAULT 0,
                markets_covered TEXT,
                providers_covered TEXT,
                status TEXT NOT NULL,
                notes TEXT
            );
        """)

        # 2. Visibility Observations Table (Per-question, per-day)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visibility_observations (
                observation_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                check_date TEXT NOT NULL,
                day_number INTEGER NOT NULL,
                market TEXT NOT NULL,
                location_setting TEXT NOT NULL,
                google_position TEXT NOT NULL,
                google_numeric_rank INTEGER,
                incubrix_ranking_url TEXT,
                featured_snippet_present INTEGER DEFAULT 0,
                paa_present INTEGER DEFAULT 0,
                ai_overview_present INTEGER DEFAULT 0,
                answer_box_type TEXT,
                quoted_source_url TEXT,
                chatgpt_status TEXT NOT NULL,
                gemini_status TEXT NOT NULL,
                perplexity_status TEXT NOT NULL,
                claude_status TEXT NOT NULL,
                competitors_named TEXT,
                raw_answers_url TEXT,
                collection_status TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES collection_runs(run_id)
            );
        """)

        # 3. Raw Provider Responses Table (Granular response texts per provider per question)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_provider_responses (
                response_id TEXT PRIMARY KEY,
                observation_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                model_version TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                market TEXT NOT NULL,
                location_setting TEXT NOT NULL,
                raw_response_text TEXT,
                response_hash TEXT NOT NULL,
                incubrix_mentioned INTEGER DEFAULT 0,
                incubrix_cited INTEGER DEFAULT 0,
                collection_status TEXT NOT NULL,
                error_message TEXT,
                FOREIGN KEY (observation_id) REFERENCES visibility_observations(observation_id)
            );
        """)

        # 4. Citations Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                citation_id TEXT PRIMARY KEY,
                observation_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                citation_url TEXT NOT NULL,
                citation_domain TEXT,
                anchor_context TEXT,
                is_incubrix INTEGER DEFAULT 0,
                FOREIGN KEY (observation_id) REFERENCES visibility_observations(observation_id)
            );
        """)

        # 5. Competitor Mentions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitor_mentions (
                mention_id TEXT PRIMARY KEY,
                observation_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                competitor_name TEXT NOT NULL,
                competitor_domain TEXT,
                context_snippet TEXT,
                FOREIGN KEY (observation_id) REFERENCES visibility_observations(observation_id)
            );
        """)

        # 6. Collection Errors Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collection_errors (
                error_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                question_id TEXT,
                provider TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                resolved_by_fallback INTEGER DEFAULT 0,
                FOREIGN KEY (run_id) REFERENCES collection_runs(run_id)
            );
        """)

        self.conn.commit()

    def insert_run(self, run_data: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO collection_runs (
                run_id, run_type, day_number, started_at, finished_at,
                input_size, successful_checks, failed_checks,
                markets_covered, providers_covered, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_data["run_id"],
            run_data["run_type"],
            run_data["day_number"],
            run_data["started_at"],
            run_data.get("finished_at"),
            run_data["input_size"],
            run_data.get("successful_checks", 0),
            run_data.get("failed_checks", 0),
            run_data.get("markets_covered", ""),
            run_data.get("providers_covered", ""),
            run_data["status"],
            run_data.get("notes", "")
        ))
        self.conn.commit()

    def insert_observation(self, obs: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO visibility_observations (
                observation_id, run_id, question_id, check_date, day_number,
                market, location_setting, google_position, google_numeric_rank,
                incubrix_ranking_url, featured_snippet_present, paa_present,
                ai_overview_present, answer_box_type, quoted_source_url,
                chatgpt_status, gemini_status, perplexity_status, claude_status,
                competitors_named, raw_answers_url, collection_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            obs["observation_id"],
            obs["run_id"],
            obs["question_id"],
            obs["check_date"],
            obs["day_number"],
            obs["market"],
            obs["location_setting"],
            obs["google_position"],
            obs.get("google_numeric_rank"),
            obs.get("incubrix_ranking_url"),
            obs.get("featured_snippet_present", 0),
            obs.get("paa_present", 0),
            obs.get("ai_overview_present", 0),
            obs.get("answer_box_type", "None"),
            obs.get("quoted_source_url"),
            obs["chatgpt_status"],
            obs["gemini_status"],
            obs["perplexity_status"],
            obs["claude_status"],
            obs.get("competitors_named", ""),
            obs.get("raw_answers_url", ""),
            obs.get("collection_status", "Success")
        ))
        self.conn.commit()

    def insert_raw_response(self, resp: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO raw_provider_responses (
                response_id, observation_id, question_id, provider,
                model_version, checked_at, market, location_setting,
                raw_response_text, response_hash, incubrix_mentioned,
                incubrix_cited, collection_status, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resp["response_id"],
            resp["observation_id"],
            resp["question_id"],
            resp["provider"],
            resp["model_version"],
            resp["checked_at"],
            resp["market"],
            resp["location_setting"],
            resp.get("raw_response_text", ""),
            resp["response_hash"],
            resp.get("incubrix_mentioned", 0),
            resp.get("incubrix_cited", 0),
            resp.get("collection_status", "Success"),
            resp.get("error_message")
        ))
        self.conn.commit()

    def insert_citation(self, cit: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO citations (
                citation_id, observation_id, question_id, provider,
                citation_url, citation_domain, anchor_context, is_incubrix
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cit["citation_id"],
            cit["observation_id"],
            cit["question_id"],
            cit["provider"],
            cit["citation_url"],
            cit.get("citation_domain", ""),
            cit.get("anchor_context", ""),
            cit.get("is_incubrix", 0)
        ))
        self.conn.commit()

    def insert_competitor_mention(self, comp: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO competitor_mentions (
                mention_id, observation_id, question_id, provider,
                competitor_name, competitor_domain, context_snippet
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            comp["mention_id"],
            comp["observation_id"],
            comp["question_id"],
            comp["provider"],
            comp["competitor_name"],
            comp.get("competitor_domain", ""),
            comp.get("context_snippet", "")
        ))
        self.conn.commit()

    def insert_error(self, err: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO collection_errors (
                error_id, run_id, question_id, provider,
                error_type, error_message, occurred_at, resolved_by_fallback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            err["error_id"],
            err["run_id"],
            err.get("question_id"),
            err["provider"],
            err["error_type"],
            err["error_message"],
            err["occurred_at"],
            err.get("resolved_by_fallback", 0)
        ))
        self.conn.commit()

    def get_all_observations(self, day_number: Optional[int] = None) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        if day_number is not None:
            cursor.execute("SELECT * FROM visibility_observations WHERE day_number = ? ORDER BY question_id", (day_number,))
        else:
            cursor.execute("SELECT * FROM visibility_observations ORDER BY day_number, question_id")
        return [dict(row) for row in cursor.fetchall()]

    def get_competitor_mention_counts(self) -> Dict[str, int]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT competitor_name, COUNT(DISTINCT question_id) as query_count
            FROM competitor_mentions
            GROUP BY competitor_name
            ORDER BY query_count DESC
        """)
        return {row["competitor_name"]: row["query_count"] for row in cursor.fetchall()}

    def get_run_history(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM collection_runs ORDER BY started_at")
        return [dict(row) for row in cursor.fetchall()]
