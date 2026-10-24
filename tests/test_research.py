"""
Automated Test Suite for Phase 1: Product Research & Question Discovery
Tests data integrity, schema compliance, category distribution, duplicate detection, and verification rules.
"""

import pytest
import pandas as pd
from typing import Dict, Any

from src.research.product_observations import get_product_observations, PRODUCT_OBSERVATIONS
from src.research.opportunity_analysis import get_growth_opportunities, GROWTH_OPPORTUNITIES
from src.research.collect_questions import (
    get_verified_questions,
    get_source_register,
    VERIFIED_QUESTIONS,
    SOURCE_REGISTER
)
from src.research.deduplicate_questions import (
    deduplicate_dataset,
    normalize_question_text,
    calculate_jaccard_similarity
)
from src.research.validate_questions import (
    validate_questions_dataframe,
    is_valid_url,
    is_valid_iso_date,
    MANDATORY_FIELDS,
    APPROVED_CATEGORIES
)


class TestProductObservations:
    def test_five_observations_count(self):
        obs = get_product_observations()
        assert len(obs) == 5, f"Expected exactly 5 observations, got {len(obs)}"

    def test_observations_schema_and_types(self):
        required_fields = [
            "observation_id",
            "feature_area",
            "what_observed",
            "evidence_url",
            "date_checked",
            "why_matters_to_creators",
            "seo_aeo_geo_implication",
            "confidence_level",
            "limitations"
        ]
        obs = get_product_observations()
        for idx, item in enumerate(obs):
            for field in required_fields:
                assert field in item, f"Observation {idx+1} missing required field '{field}'"
                assert str(item[field]).strip() != "", f"Observation {item['observation_id']} field '{field}' is empty"
            assert is_valid_url(item["evidence_url"]), f"Invalid evidence URL in {item['observation_id']}"
            assert is_valid_iso_date(item["date_checked"]), f"Invalid date in {item['observation_id']}"


class TestGrowthOpportunities:
    def test_three_opportunities_count(self):
        opps = get_growth_opportunities()
        assert len(opps) == 3, f"Expected exactly 3 opportunities, got {len(opps)}"

    def test_opportunities_schema(self):
        required_fields = [
            "opportunity_id",
            "title",
            "target_audience",
            "user_problem",
            "relevant_question_cluster",
            "existing_evidence_of_demand",
            "potential_business_value",
            "current_visibility_gap",
            "recommended_action",
            "how_success_measured",
            "target_30_day"
        ]
        opps = get_growth_opportunities()
        for idx, item in enumerate(opps):
            for field in required_fields:
                assert field in item, f"Opportunity {idx+1} missing field '{field}'"
                assert str(item[field]).strip() != "", f"Opportunity {item['opportunity_id']} field '{field}' is empty"


class TestSourceRegister:
    def test_source_register_not_empty(self):
        sources = get_source_register()
        assert len(sources) >= 5, f"Expected at least 5 registered sources, got {len(sources)}"

    def test_source_register_fields(self):
        for s in get_source_register():
            assert "source_id" in s
            assert "source_name" in s
            assert "source_type" in s
            assert "legitimate_proof" in s
            assert "limitations" in s
            assert "verification_protocol" in s


class TestQuestionsDataset:
    @pytest.fixture
    def questions_df(self):
        return pd.DataFrame(get_verified_questions())

    def test_question_count_is_100(self, questions_df):
        assert len(questions_df) == 100, f"Expected exactly 100 questions, got {len(questions_df)}"

    def test_mandatory_columns_present(self, questions_df):
        for col in MANDATORY_FIELDS:
            assert col in questions_df.columns, f"Missing required column: '{col}'"

    def test_no_empty_mandatory_cells(self, questions_df):
        for col in MANDATORY_FIELDS:
            empty_count = questions_df[col].isna().sum() + (questions_df[col].astype(str).str.strip() == "").sum()
            assert empty_count == 0, f"Column '{col}' has {empty_count} empty cells"

    def test_category_distribution_and_balance(self, questions_df):
        categories = questions_df["category"].unique().tolist()
        assert len(categories) == 10, f"Expected exactly 10 categories, got {len(categories)}"
        for cat in APPROVED_CATEGORIES:
            assert cat in categories, f"Approved category '{cat}' not found in dataset"
            count = (questions_df["category"] == cat).sum()
            assert count >= 8, f"Category '{cat}' has insufficient count: {count} (minimum 8 required)"

    def test_all_urls_valid(self, questions_df):
        for idx, r in questions_df.iterrows():
            assert is_valid_url(r["source_url"]), f"Invalid URL for {r['question_id']}: {r['source_url']}"

    def test_all_dates_valid(self, questions_df):
        for idx, r in questions_df.iterrows():
            assert is_valid_iso_date(r["collection_date"]), f"Invalid date for {r['question_id']}: {r['collection_date']}"

    def test_evidence_verification_integrity(self, questions_df):
        for idx, r in questions_df.iterrows():
            evidence = str(r["source_evidence"]).strip()
            assert len(evidence) >= 10, f"Question {r['question_id']} evidence too short: '{evidence}'"
            assert evidence != r["source_url"], f"Question {r['question_id']} evidence just repeats source URL"


class TestDeduplication:
    def test_no_exact_duplicates_in_dataset(self):
        df = pd.DataFrame(get_verified_questions())
        cleaned, report = deduplicate_dataset(df)
        assert report["exact_duplicates_count"] == 0, f"Found exact duplicates: {report['exact_duplicates']}"
        assert len(cleaned) == 100

    def test_normalizer_behavior(self):
        raw = "How to Turn LONG Videos Into Short TikTok Clips With AI??? "
        norm = normalize_question_text(raw)
        assert norm == "how to turn long videos into short tiktok clips with ai"

    def test_deduplicator_catches_synthetic_duplicate(self):
        df = pd.DataFrame([
            {"question_id": "T1", "question_text": "What is the best AI video editor?"},
            {"question_id": "T2", "question_text": "what is the best ai video editor??? "},
            {"question_id": "T3", "question_text": "How to create shorts with AI?"}
        ])
        cleaned, report = deduplicate_dataset(df)
        assert report["total_records"] == 3
        assert report["unique_records"] == 2
        assert report["exact_duplicates_count"] == 1
        assert report["exact_duplicates"][0]["duplicate_id"] == "T2"

    def test_near_duplicate_jaccard(self):
        q1 = "Best AI tool to convert podcast video into reels"
        q2 = "Best AI tools to convert podcast videos into reels"
        sim = calculate_jaccard_similarity(q1, q2)
        assert sim >= 0.80


class TestFullValidationPipeline:
    def test_validation_report_returns_valid(self):
        df = pd.DataFrame(get_verified_questions())
        report = validate_questions_dataframe(df)
        assert report["is_valid"] is True, f"Validation failed: {report['validation_errors']}"
        assert report["status_summary"]["verified"] == 100
        assert report["status_summary"]["rejected"] == 0
        assert len(report["deficient_categories"]) == 0

    def test_validation_flags_invalid_row(self):
        bad_df = pd.DataFrame([
            {
                "question_id": "BAD01",
                "question_text": "Is this valid?",
                "category": "Invalid Category",
                "subcategory": "None",
                "source_type": "None",
                "source_name": "None",
                "source_url": "not-a-url",
                "collection_date": "2026-99-99",
                "search_intent": "Informational",
                "target_audience": "Creators",
                "relevant_market": "US",
                "relevance_to_incubrix": "None",
                "source_evidence": "",
                "verification_status": "Verified",
                "notes": "None"
            }
        ])
        report = validate_questions_dataframe(bad_df)
        assert report["is_valid"] is False
        assert report["status_summary"]["rejected"] == 1
        assert len(report["validation_errors"]["url_errors"]) > 0
        assert len(report["validation_errors"]["date_errors"]) > 0
        assert len(report["validation_errors"]["category_errors"]) > 0
