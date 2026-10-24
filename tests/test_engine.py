"""
Automated Test Suite for Phase 6: Automated Visibility Engine
Tests data ingestion, schema validation, observation persistence,
historical record preservation, metric formulas, citation/mention separation,
duplicate prevention, weekly report generation, and content brief generation.
"""

import os
import json
import sqlite3
import pytest
import pandas as pd

from src.engine.database import EngineDatabase
from src.engine.ingestion import DataIngestor
from src.engine.metrics import EngineMetrics
from src.engine.weekly_reporter import WeeklyReporter
from src.engine.brief_generator import ContentBriefGenerator
from src.engine.scheduler import RefreshWorkflow


class TestEngineDatabaseAndIngestion:
    @pytest.fixture(scope="module")
    def db(self):
        return EngineDatabase()

    def test_all_thirteen_tables_exist(self, db):
        counts = db.get_table_counts()
        expected_tables = [
            "collection_runs", "visibility_observations", "raw_provider_responses",
            "citations", "competitor_mentions", "collection_errors",
            "questions", "sources", "audit_findings", "recommended_fixes",
            "content_pages", "citation_opportunities", "validation_results"
        ]
        for t in expected_tables:
            assert t in counts, f"Missing table {t} in database"
            assert counts[t] >= 0, f"Table {t} returned error count"

    def test_question_import_count_is_one_hundred(self, db):
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM questions;")
        count = cursor.fetchone()[0]
        assert count == 100, f"Expected 100 questions, found {count}"

    def test_historical_observations_preserved_across_runs(self, db):
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM visibility_observations WHERE day_number = 1;")
        d1 = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM visibility_observations WHERE day_number = 2;")
        d2 = cursor.fetchone()[0]
        assert d1 == 100, f"Day 1 observations missing: {d1}"
        assert d2 == 100, f"Day 2 observations missing: {d2}"

    def test_duplicate_prevention_on_ingestion(self, db):
        ingestor = DataIngestor(db)
        # Running sync_all twice should not increase question count
        initial_count = db.get_table_counts()["questions"]
        ingestor.sync_questions()
        post_count = db.get_table_counts()["questions"]
        assert initial_count == post_count, "Duplicate questions inserted on re-ingestion"


class TestVisibilityFormulasAndMetrics:
    @pytest.fixture(scope="module")
    def em(self):
        return EngineMetrics()

    def test_baseline_organic_visibility_score_zero(self, em):
        metrics = em.get_summary_metrics()
        assert metrics["organic_visibility_score"] == 0.0, "Expected 0.0% organic visibility for IncuBrix"

    def test_ai_overview_presence_rate(self, em):
        metrics = em.get_summary_metrics()
        assert 60.0 <= metrics["ai_overview_presence_rate"] <= 65.0

    def test_featured_snippet_rate(self, em):
        metrics = em.get_summary_metrics()
        assert 20.0 <= metrics["featured_snippet_rate"] <= 30.0

    def test_paa_presence_rate(self, em):
        metrics = em.get_summary_metrics()
        assert 10.0 <= metrics["paa_presence_rate"] <= 25.0

    def test_citation_and_mention_separation(self, em):
        cursor = em.db.conn.cursor()
        # Ensure citations and mentions are tracked separately
        cursor.execute("SELECT COUNT(*) FROM citations;")
        cit_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM competitor_mentions;")
        men_count = cursor.fetchone()[0]
        assert cit_count > 0
        assert men_count > 0
        assert cit_count != men_count

    def test_competitor_share_of_voice_ranking(self, em):
        metrics = em.get_summary_metrics()
        comps = metrics["top_competitors"]
        assert len(comps) >= 3
        # OpusClip and Descript should lead
        names = [c["name"] for c in comps]
        assert "OpusClip" in names
        assert "Descript" in names


class TestWeeklyReportingAndBriefGenerator:
    def test_weekly_report_generation(self):
        wr = WeeklyReporter()
        paths = wr.generate_report(report_date="2026-10-24")
        assert os.path.exists(paths["json_report"])
        assert os.path.exists(paths["markdown_report"])

        # Validate JSON content
        with open(paths["json_report"], "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["report_id"] == "REP-2026-10-24"
        assert "baseline_visibility_metrics" in data
        assert "competitor_share_of_voice" in data
        wr.db.close()

    def test_content_brief_generation_for_valid_question(self):
        cbg = ContentBriefGenerator()
        brief = cbg.generate_brief_for_question("Q021")
        assert brief["question_id"] == "Q021"
        assert "turn long" in brief["primary_question"].lower()
        assert os.path.exists(brief["markdown_path"])
        with open(brief["markdown_path"], "r", encoding="utf-8") as f:
            content = f.read()
        assert "AEO & AI Overview Target" in content
        assert "Verified IncuBrix Anchors" in content
        cbg.db.close()

    def test_content_brief_raises_keyerror_for_invalid_question(self):
        cbg = ContentBriefGenerator()
        with pytest.raises(KeyError):
            cbg.generate_brief_for_question("Q999")
        cbg.db.close()


class TestSchedulerAndErrorHandling:
    def test_refresh_cycle_creates_collection_run(self):
        rw = RefreshWorkflow()
        res = rw.execute_refresh_cycle(scope="TEST_SCOPE")
        assert res["status"] == "COMPLETED"
        assert res["run_id"].startswith("RUN-")
        rw.db.close()

    def test_missing_data_handling_in_metrics(self):
        # Empty database instance should return sensible defaults without crashing
        mem_db = EngineDatabase(":memory:")
        em = EngineMetrics(mem_db)
        metrics = em.get_summary_metrics()
        assert metrics["total_questions"] == 0
        assert metrics["organic_visibility_score"] == 0.0
        mem_db.close()
