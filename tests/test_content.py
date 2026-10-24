"""
Automated Test Suite for Phase 4: Publish-Ready SEO, AEO & GEO Pages
Tests topic selection, metadata generation, direct answer presence,
schema validation, word counts, content register, and workbook tab 02c_PAGES_CITATIONS.
"""

import os
import re
import json
import pytest
import pandas as pd
import openpyxl

from src.content.topic_selector import TopicSelector, SELECTED_TOPICS
from src.content.metadata_generator import MetadataGenerator
from src.content.schema_generator import SchemaGenerator
from src.content.fact_checker import FactChecker
from src.content.internal_links import InternalLinkManager
from src.content.page_generator import PageGenerator
from src.content.publishing_validator import PublishingValidator


class TestTopicSelection:
    def test_exactly_ten_topics_selected(self):
        assert len(SELECTED_TOPICS) == 10

    def test_unique_page_ids_and_slugs(self):
        ids = [t["page_id"] for t in SELECTED_TOPICS]
        slugs = [t["slug"] for t in SELECTED_TOPICS]
        assert len(set(ids)) == 10
        assert len(set(slugs)) == 10
        for i in range(1, 11):
            assert f"P{i:02d}" in ids

    def test_topic_mix_diversity(self):
        res = TopicSelector.validate_topic_mix()
        assert res["is_valid"] is True
        assert res["content_types_count"] >= 4
        # Verify specific required content types are represented
        types = [t["content_type"] for t in SELECTED_TOPICS]
        assert any("How-to" in t for t in types)
        assert any("Comparison" in t for t in types)
        assert any("FAQ" in t or "Frequently" in t for t in types)
        assert any("Glossary" in t for t in types)
        assert any("Workflow" in t for t in types)

    def test_all_topics_have_selection_rationale(self):
        for t in SELECTED_TOPICS:
            assert len(t["selection_rationale"].strip()) > 50
            assert len(t["target_question_ids"]) >= 1


class TestContentGenerationAndValidation:
    @pytest.fixture(scope="module")
    def generated_pages(self):
        return PageGenerator.generate_all_pages()

    def test_exactly_ten_pages_generated(self, generated_pages):
        assert len(generated_pages) == 10

    def test_markdown_files_exist_in_outputs_and_submission(self, generated_pages):
        for i in range(1, 11):
            out_file = f"outputs/pages/page_{i:02d}.md"
            assert os.path.exists(out_file), f"Missing {out_file}"
            assert os.path.getsize(out_file) > 2000, f"File {out_file} is suspiciously small"

        # Check submission files exist
        for t in SELECTED_TOPICS:
            sub_file = f"submission/content/{t['page_id']}_{t['slug']}.md"
            assert os.path.exists(sub_file), f"Missing {sub_file}"

    def test_all_pages_pass_publishing_validator(self, generated_pages):
        report = PublishingValidator.validate_all_pages("outputs/pages")
        assert report["all_valid"] is True, f"Validation errors found: {report['results']}"
        assert report["valid_count"] == 10

    def test_word_counts_exceed_800_words(self, generated_pages):
        for i in range(1, 11):
            fp = f"outputs/pages/page_{i:02d}.md"
            res = PublishingValidator.validate_page_file(fp)
            assert res["word_count"] >= 800, f"Page {fp} has only {res['word_count']} words"

    def test_direct_answer_present_in_opening_two_sentences(self, generated_pages):
        for i in range(1, 11):
            fp = f"outputs/pages/page_{i:02d}.md"
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            assert "Quick Answer (AEO / Direct Answer)" in content, f"Page {fp} missing AEO quick answer block"
            match = re.search(r'> \*\*Quick Answer.*?\*\*:\s*\n>\s*(.+?)(?=\n\n|\n---)', content, re.DOTALL)
            assert match is not None, f"Could not extract quick answer from {fp}"
            answer_text = match.group(1).strip()
            # Ensure answer contains substance
            assert len(answer_text) > 50

    def test_json_ld_schemas_parse_validly(self, generated_pages):
        for i in range(1, 11):
            fp = f"outputs/pages/page_{i:02d}.md"
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
            assert len(matches) >= 1, f"Missing JSON-LD in {fp}"
            for m in matches:
                data = json.loads(m.strip())
                assert "@context" in data
                assert "@graph" in data
                assert len(data["@graph"]) >= 2  # Article + BreadcrumbList + additional


class TestContentRegisterAndWorkbook:
    def test_content_register_csv_export(self):
        pages = PageGenerator.generate_all_pages()
        csv_path = PageGenerator.export_content_register_csv(pages)
        assert os.path.exists(csv_path)
        df = pd.read_csv(csv_path)
        assert len(df) == 10
        assert "page_id" in df.columns
        assert "seo_title" in df.columns
        assert "h1_heading" in df.columns
        assert "target_opportunity" in df.columns

    def test_workbook_tab_02c_populated(self):
        pages = PageGenerator.generate_all_pages()
        wb_path = PageGenerator.populate_workbook_tab_02c(pages)
        assert os.path.exists(wb_path)
        wb = openpyxl.load_workbook(wb_path, data_only=True)
        assert "02c_PAGES_CITATIONS" in wb.sheetnames
        sheet = wb["02c_PAGES_CITATIONS"]
        # Rows 5 to 14 correspond to P01 to P10
        for idx in range(10):
            row = 5 + idx
            expected_id = f"P{idx+1:02d}"
            assert sheet.cell(row, 1).value == expected_id
            assert sheet.cell(row, 2).value == "Publish-Ready Page"
            assert sheet.cell(row, 9).value == "Publish-Ready"


class TestFactCheckingAndInternalLinks:
    def test_verified_sources_have_valid_urls(self):
        sources = FactChecker.get_verified_sources()
        assert len(sources) >= 5
        valid, errors = FactChecker.check_citation_traceability(sources)
        assert valid is True, f"Citation errors: {errors}"

    def test_forbidden_superlatives_detector(self):
        bad_text = "This is the best tool in the world and 100% viral rate guaranteed!"
        violations = FactChecker.check_text_for_superlatives(bad_text)
        assert len(violations) >= 2

    def test_internal_link_manager_returns_verified_targets(self):
        verified_urls = InternalLinkManager.get_verified_urls()
        assert "https://incubrix.com/" in verified_urls
        assert "https://incubrix.com/pricing" in verified_urls
        assert "https://app.incubrix.com" in verified_urls
        for i in range(1, 11):
            pid = f"P{i:02d}"
            links = InternalLinkManager.get_contextual_links_for_page(pid)
            assert len(links) >= 3
            for l in links:
                assert l["url"].startswith("https://")
                assert len(l["anchor"]) > 5
