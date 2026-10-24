"""
Automated Test Suite for Phase 2: SEO, AEO, and GEO Visibility Baseline
Tests database integrity, adapter logic, mention vs citation separation, metric calculations,
two-day variance, missing value handling, and error logging.
"""

import os
import pytest
import sqlite3
import pandas as pd

from src.visibility.database import VisibilityDatabase
from src.visibility.adapters import BaseAdapter, GoogleSearchAdapter, PerplexityAdapter
from src.visibility.collector import VisibilityCollector
from src.visibility.baseline_exporter import export_visibility_csv, WORKBOOK_COLUMNS
from src.visibility.metrics_calculator import VisibilityMetricsCalculator


@pytest.fixture(scope="module")
def initialized_db():
    collector = VisibilityCollector(
        db_path="data/visibility.db",
        evidence_dir="evidence/raw",
        questions_csv="data/research/questions.csv"
    )
    collector.run_two_day_baseline_collection()
    export_visibility_csv()
    return VisibilityDatabase("data/visibility.db")


class TestDatabaseIntegrity:
    def test_six_tables_exist(self, initialized_db):
        cursor = initialized_db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = [
            "collection_runs",
            "visibility_observations",
            "raw_provider_responses",
            "citations",
            "competitor_mentions",
            "collection_errors"
        ]
        for tbl in expected_tables:
            assert tbl in tables, f"Expected table '{tbl}' not found in SQLite database"

    def test_two_day_observation_counts(self, initialized_db):
        obs_d1 = initialized_db.get_all_observations(day_number=1)
        obs_d2 = initialized_db.get_all_observations(day_number=2)
        assert len(obs_d1) == 100, f"Expected 100 observations on Day 1, found {len(obs_d1)}"
        assert len(obs_d2) == 100, f"Expected 100 observations on Day 2, found {len(obs_d2)}"

    def test_raw_provider_responses_count(self, initialized_db):
        cursor = initialized_db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM raw_provider_responses;")
        total_raw = cursor.fetchone()[0]
        # 200 observations * 5 providers = 1000 raw responses
        assert total_raw == 1000, f"Expected 1000 raw provider responses, found {total_raw}"

    def test_collection_runs_recorded(self, initialized_db):
        runs = initialized_db.get_run_history()
        assert len(runs) >= 2, f"Expected at least 2 collection runs, found {len(runs)}"
        run_ids = [r["run_id"] for r in runs]
        assert "RUN-20261021-DAY1" in run_ids
        assert "RUN-20261023-DAY2" in run_ids


class TestAdaptersAndMentionCitationLogic:
    def test_detect_brand_mention(self):
        text_with = "You can use IncuBrix or OpusClip to generate short clips."
        text_without = "You can use OpusClip, Descript, or Klap."
        assert BaseAdapter.detect_brand_mention(text_with, "IncuBrix") is True
        assert BaseAdapter.detect_brand_mention(text_without, "IncuBrix") is False

    def test_detect_brand_citation(self):
        urls_with = ["https://zapier.com/blog", "https://incubrix.com/features"]
        urls_without = ["https://zapier.com/blog", "https://opus.pro"]
        assert BaseAdapter.detect_brand_citation(urls_with, "incubrix.com") is True
        assert BaseAdapter.detect_brand_citation(urls_without, "incubrix.com") is False

    def test_mention_does_not_imply_citation(self):
        # Text mentions IncuBrix, but citation URLs do not contain it
        text = "IncuBrix is a promising tool, but Zapier recommends OpusClip."
        citations = ["https://zapier.com/blog/best-ai-video-generators/"]
        assert BaseAdapter.detect_brand_mention(text, "IncuBrix") is True
        assert BaseAdapter.detect_brand_citation(citations, "incubrix.com") is False

    def test_extract_competitors(self):
        text = "Top tools include OpusClip, Descript, Kapwing, and Veed.io."
        comps = BaseAdapter.extract_competitors(text)
        assert "OpusClip" in comps
        assert "Descript" in comps
        assert "Kapwing" in comps
        assert "Veed.io" in comps


class TestVisibilityCSVExport:
    @pytest.fixture
    def visibility_df(self):
        assert os.path.exists("data/visibility.csv")
        return pd.read_csv("data/visibility.csv", keep_default_na=False)

    def test_csv_has_exactly_100_rows(self, visibility_df):
        assert len(visibility_df) == 100, f"Expected 100 rows in visibility.csv, found {len(visibility_df)}"

    def test_all_20_columns_present(self, visibility_df):
        for col in WORKBOOK_COLUMNS:
            assert col in visibility_df.columns, f"Missing required column in visibility.csv: '{col}'"

    def test_no_duplicate_questions_in_export(self, visibility_df):
        dups = visibility_df["question_id"].duplicated().sum()
        assert dups == 0, f"Found {dups} duplicate question IDs in visibility.csv"

    def test_no_null_critical_cells(self, visibility_df):
        critical_cols = [
            "question_id", "question", "market", "google_position",
            "answer_box_or_ai_overview", "chatgpt", "gemini",
            "perplexity", "claude_or_copilot", "check_date_day1", "check_date_day2"
        ]
        for col in critical_cols:
            empty_count = (visibility_df[col] == "").sum()
            assert empty_count == 0, f"Column '{col}' has {empty_count} empty values in visibility.csv"

    def test_markets_coverage_in_dataset(self, visibility_df):
        markets = visibility_df["market"].unique().tolist()
        assert "US" in markets
        # At least 2 additional markets covered
        assert len(markets) >= 3, f"Expected at least 3 markets, got: {markets}"


class TestMetricsCalculation:
    @pytest.fixture
    def metrics(self):
        calc = VisibilityMetricsCalculator("data/visibility.db")
        return calc.calculate_all_metrics()

    def test_organic_visibility_score_zero(self, metrics):
        # All questions currently rank >100, so score should be 0.0%
        org = metrics["organic_visibility"]
        assert org["score_pct"] == 0.0
        assert org["ranked_questions_count"] == 0
        assert org["unranked_questions_count"] == 100

    def test_featured_snippet_presence_rate(self, metrics):
        fs = metrics["featured_snippet"]
        assert 0.0 <= fs["presence_rate_pct"] <= 100.0
        assert fs["total_valid_queries"] == 100

    def test_paa_presence_rate(self, metrics):
        paa = metrics["people_also_ask"]
        assert 0.0 <= paa["presence_rate_pct"] <= 100.0
        assert paa["count"] == 16

    def test_ai_overview_metrics(self, metrics):
        aio = metrics["ai_overview"]
        assert aio["presence_rate_pct"] > 0.0
        assert aio["citation_rate_pct"] == 0.0  # IncuBrix currently has 0 citations

    def test_ai_assistant_mention_and_citation_rates(self, metrics):
        ai = metrics["ai_assistants"]
        assert ai["overall_mention_rate_pct"] == 0.0
        assert ai["overall_citation_rate_pct"] == 0.0
        assert ai["total_checks"] == 400

    def test_two_day_variance_bounds(self, metrics):
        var = metrics["two_day_variance"]
        assert 0.0 <= var["variance_rate_pct"] <= 10.0
        assert var["stability_rate_pct"] >= 90.0

    def test_competitor_analysis_presence(self, metrics):
        comps = metrics["competitor_analysis"]
        assert "OpusClip" in comps
        assert "Descript" in comps
        assert comps["OpusClip"]["count"] >= 40


class TestErrorHandlingAndFallbacks:
    def test_error_logging_table(self):
        db = VisibilityDatabase("data/visibility.db")
        # Insert a simulated error
        err = {
            "error_id": "ERR-TEST-SIMULATED",
            "run_id": "RUN-20261021-DAY1",
            "question_id": "Q001",
            "provider": "TestProvider",
            "error_type": "RateLimitExceeded",
            "error_message": "HTTP 429 Too Many Requests (mock simulation)",
            "occurred_at": "2026-10-21T10:00:00Z",
            "resolved_by_fallback": 1
        }
        db.insert_error(err)

        cursor = db.conn.cursor()
        cursor.execute("SELECT * FROM collection_errors WHERE error_id = 'ERR-TEST-SIMULATED';")
        row = cursor.fetchone()
        assert row is not None
        assert row["error_type"] == "RateLimitExceeded"
        assert row["resolved_by_fallback"] == 1
