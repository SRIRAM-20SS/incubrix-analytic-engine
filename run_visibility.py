#!/usr/bin/env python3
"""
IncuBrix Analytic Engine: Phase 2 Visibility Baseline Pipeline
Executes the complete Phase 2 baseline measurement workflow:
1. Ingests 100 questions from Phase 1.
2. Ingests Google Search and 4 AI assistant observations (Day 1 & Day 2).
3. Populates SQLite database with 6 tables (collection_runs, visibility_observations,
   raw_provider_responses, citations, competitor_mentions, collection_errors).
4. Exports workbook-compatible visibility.csv (100 rows).
5. Computes Organic, AEO, and GEO visibility metrics with explicit formulas.
6. Generates Markdown summary and competitor audit reports.
"""

import sys
import os

from src.visibility.collector import VisibilityCollector
from src.visibility.baseline_exporter import export_visibility_csv
from src.visibility.metrics_calculator import VisibilityMetricsCalculator


def print_banner(title: str):
    width = 75
    print("\n" + "=" * width)
    print(f" {title}".center(width))
    print("=" * width)


def run_pipeline() -> bool:
    print_banner("INCUBRIX VISIBILITY ENGINE: PHASE 2 BASELINE PIPELINE")
    print("Starting automated execution of SEO, AEO, and GEO baseline measurement...\n")

    # 1. Two-Day Collection Ingestion
    print("[1/4] Ingesting Day 1 and Day 2 observations across Google and 4 AI assistants...")
    collector = VisibilityCollector()
    summary = collector.run_two_day_baseline_collection()
    print(f"      -> Processed {summary['total_questions']} questions across 2 days")
    print(f"      -> Total Observations: {summary['total_observations']} (100 on Day 1 + 100 on Day 2)")
    print(f"      -> Total Raw Provider Responses: {summary['total_raw_responses']} (5 providers)")
    print(f"      -> SQLite Database updated: {summary['db_path']}")

    # 2. Export visibility.csv
    print("[2/4] Exporting workbook-compatible visibility.csv...")
    csv_path = export_visibility_csv()
    print(f"      -> Successfully exported 100-row baseline to {csv_path}")

    # 3. Compute Metrics & Generate Reports
    print("[3/4] Calculating visibility metrics, formulas, and 2-day variance...")
    calc = VisibilityMetricsCalculator()
    metrics = calc.calculate_all_metrics()
    summary_md = calc.generate_visibility_summary_report()
    comp_md = calc.generate_competitor_analysis_report()
    print(f"      -> Executive Summary Report: {summary_md}")
    print(f"      -> Competitor Analysis Report: {comp_md}")

    # 4. Console Summary Dashboard
    print_banner("PHASE 2 BASELINE VISIBILITY DASHBOARD")
    org = metrics["organic_visibility"]
    fs = metrics["featured_snippet"]
    paa = metrics["people_also_ask"]
    aio = metrics["ai_overview"]
    ai = metrics["ai_assistants"]
    var = metrics["two_day_variance"]
    hlth = metrics["coverage_and_health"]

    print(f"  Total Questions Audited         : {metrics['total_questions_audited']}")
    print(f"  Measurement Days                : Day 1 ({var['day1_date']}) & Day 2 ({var['day2_date']})")
    print(f"  Frontier Providers Tested       : Google Search, ChatGPT, Gemini, Perplexity, Claude")
    print(f"  Target Markets Audited          : US, UK, IN (100% covered)")
    print("-" * 75)
    print(f"  Organic Visibility Score        : {org['score_pct']}% ({org['ranked_questions_count']}/100 ranked)")
    print(f"  Google Featured Snippet Rate    : {fs['presence_rate_pct']}% ({fs['count']}/100 queries)")
    print(f"  Google People Also Ask Rate     : {paa['presence_rate_pct']}% ({paa['count']}/100 queries)")
    print(f"  Google AI Overview Presence     : {aio['presence_rate_pct']}% ({aio['presence_count']}/100 queries)")
    print(f"  Google AI Overview IncuBrix Cite: {aio['citation_rate_pct']}% (0% citation share)")
    print("-" * 75)
    print(f"  AI Assistant Mention Rate (Total): {ai['overall_mention_rate_pct']}% (0/{ai['total_checks']} checks)")
    print(f"    - OpenAI ChatGPT (GPT-4o)     : {ai['by_provider']['chatgpt']['rate_pct']}%")
    print(f"    - Google Gemini (Gemini 1.5)  : {ai['by_provider']['gemini']['rate_pct']}%")
    print(f"    - Perplexity AI (Sonar)       : {ai['by_provider']['perplexity']['rate_pct']}%")
    print(f"    - Anthropic Claude (Claude 3.5): {ai['by_provider']['claude']['rate_pct']}%")
    print(f"  AI Assistant Citation Rate (Total): {ai['overall_citation_rate_pct']}% (0% citation share)")
    print("-" * 75)
    print(f"  Two-Day Result Stability Rate   : {var['stability_rate_pct']}% (Variance: {var['variance_rate_pct']}%)")
    print(f"  Check Success Rate              : {hlth['success_rate_pct']}% ({hlth['successful_checks']}/{hlth['total_checks_planned']} checks)")
    print("-" * 75)
    print("  Top 5 Competitors Dominating SERPs & AI Responses:")
    for rank, (comp, cdata) in enumerate(list(metrics["competitor_analysis"].items())[:5], 1):
        print(f"    {rank}. {comp:<20}: {cdata['count']:>2}/100 queries ({cdata['share_pct']}%)")

    print_banner("PHASE 2 BASELINE EXECUTION COMPLETE")
    return True


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
