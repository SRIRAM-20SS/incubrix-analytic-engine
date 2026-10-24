"""
IncuBrix Automated Visibility Engine: Database Manager (Phase 6)
Unified SQLite database manager implementing all 13 required persistence tables:
1. collection_runs
2. visibility_observations
3. raw_provider_responses (raw_responses)
4. citations
5. competitor_mentions
6. collection_errors (errors)
7. questions
8. sources
9. audit_findings
10. recommended_fixes
11. content_pages
12. citation_opportunities
13. validation_results
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional
import pandas as pd


class EngineDatabase:
    """Manages the master unified SQLite database for the IncuBrix Visibility Engine."""

    def __init__(self, db_path: str = "data/visibility.db"):
        self.db_path = db_path
        if self.db_path != ":memory:" and os.path.dirname(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_all_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()

    def init_all_tables(self):
        cursor = self.conn.cursor()

        # 1. Collection Runs
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

        # 2. Visibility Observations
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

        # 3. Raw Provider Responses
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

        # 4. Citations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                citation_id TEXT PRIMARY KEY,
                observation_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                citation_url TEXT NOT NULL,
                citation_domain TEXT NOT NULL,
                anchor_context TEXT,
                is_incubrix INTEGER DEFAULT 0,
                FOREIGN KEY (observation_id) REFERENCES visibility_observations(observation_id)
            );
        """)

        # 5. Competitor Mentions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitor_mentions (
                mention_id TEXT PRIMARY KEY,
                observation_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                competitor_name TEXT NOT NULL,
                provider TEXT NOT NULL,
                context_snippet TEXT,
                detected_at TEXT NOT NULL,
                FOREIGN KEY (observation_id) REFERENCES visibility_observations(observation_id)
            );
        """)

        # 6. Errors / Collection Errors
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collection_errors (
                error_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                question_id TEXT,
                provider TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_details TEXT NOT NULL,
                occurred_at TEXT NOT NULL
            );
        """)

        # 7. Questions (Phase 1 master repository)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id TEXT PRIMARY KEY,
                question_text TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                source_type TEXT,
                source_name TEXT,
                source_url TEXT,
                collection_date TEXT,
                search_intent TEXT,
                target_audience TEXT,
                relevant_market TEXT,
                relevance_to_incubrix TEXT,
                source_evidence TEXT,
                verification_status TEXT,
                notes TEXT
            );
        """)

        # 8. Sources (Phase 1 source register)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY,
                source_name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                access_method TEXT,
                legitimate_proof TEXT,
                limitations TEXT,
                question_count INTEGER,
                verification_protocol TEXT
            );
        """)

        # 9. Audit Findings (Phase 3 technical audit findings)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_findings (
                finding_id TEXT PRIMARY KEY,
                target_url TEXT NOT NULL,
                audit_category TEXT NOT NULL,
                observed_problem TEXT NOT NULL,
                evidence TEXT NOT NULL,
                date_checked TEXT NOT NULL,
                severity TEXT NOT NULL
            );
        """)

        # 10. Recommended Fixes (Phase 3 20 fixes register)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommended_fixes (
                fix_id TEXT PRIMARY KEY,
                affected_url TEXT NOT NULL,
                audit_category TEXT NOT NULL,
                priority TEXT NOT NULL,
                impact TEXT NOT NULL,
                observed_problem TEXT NOT NULL,
                recommended_solution TEXT NOT NULL,
                file_artifact TEXT,
                validation_method TEXT,
                validation_result TEXT,
                implementation_status TEXT,
                date_checked TEXT
            );
        """)

        # 11. Content Pages (Phase 4 10 publish-ready pages)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_pages (
                page_id TEXT PRIMARY KEY,
                target_opportunity TEXT NOT NULL,
                target_question_ids TEXT NOT NULL,
                slug TEXT NOT NULL,
                full_url TEXT NOT NULL,
                content_type TEXT NOT NULL,
                category TEXT NOT NULL,
                primary_keyword TEXT NOT NULL,
                seo_title TEXT NOT NULL,
                meta_description TEXT NOT NULL,
                word_count INTEGER,
                direct_answer_status TEXT,
                markdown_file TEXT NOT NULL,
                status TEXT NOT NULL
            );
        """)

        # 12. Citation Opportunities (Phase 5 30 citation targets)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citation_opportunities (
                target_id TEXT PRIMARY KEY,
                publisher_name TEXT NOT NULL,
                page_title TEXT NOT NULL,
                page_url TEXT NOT NULL,
                page_type TEXT NOT NULL,
                related_question_ids TEXT,
                target_question TEXT,
                market TEXT,
                discovery_method TEXT,
                observed_in_google TEXT,
                observed_in_ai_answer TEXT,
                priority TEXT,
                composite_score INTEGER,
                potential_inclusion_angle TEXT,
                suggested_ethical_action TEXT,
                date_checked TEXT
            );
        """)

        # 13. Validation Results (Engine QA logs)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS validation_results (
                validation_id TEXT PRIMARY KEY,
                component TEXT NOT NULL,
                check_name TEXT NOT NULL,
                status TEXT NOT NULL,
                errors_count INTEGER DEFAULT 0,
                details TEXT,
                executed_at TEXT NOT NULL
            );
        """)

        self.conn.commit()

    def get_table_counts(self) -> Dict[str, int]:
        """Returns the row count for all 13 database tables."""
        tables = [
            "collection_runs", "visibility_observations", "raw_provider_responses",
            "citations", "competitor_mentions", "collection_errors",
            "questions", "sources", "audit_findings", "recommended_fixes",
            "content_pages", "citation_opportunities", "validation_results"
        ]
        counts = {}
        cursor = self.conn.cursor()
        for t in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {t};")
                counts[t] = cursor.fetchone()[0]
            except Exception:
                counts[t] = -1
        return counts


if __name__ == "__main__":
    db = EngineDatabase()
    print("Database Initialized. Table row counts:")
    counts = db.get_table_counts()
    for t, c in counts.items():
        print(f" - {t:<26}: {c} rows")
    db.close()
