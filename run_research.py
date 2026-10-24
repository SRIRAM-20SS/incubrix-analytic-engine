#!/usr/bin/env python3
"""
IncuBrix Analytic Engine: Phase 1 Product Research and Question Discovery Pipeline
Executes the complete research workflow:
1. Product observations export
2. Strategic growth opportunities export
3. Source register export
4. 100-Question baseline export & deduplication
5. Comprehensive schema, format, category, and evidence validation
6. Automated audit report generation
"""

import os
import sys
import pandas as pd
from typing import Dict, Any

from src.research.product_observations import export_product_observations, get_product_observations
from src.research.opportunity_analysis import export_growth_opportunities, get_growth_opportunities
from src.research.collect_questions import (
    export_questions_csv,
    export_source_register_csv,
    get_verified_questions,
    get_source_register
)
from src.research.deduplicate_questions import deduplicate_dataset
from src.research.validate_questions import validate_questions_dataframe, generate_validation_report


def print_banner(title: str):
    width = 75
    print("\n" + "=" * width)
    print(f" {title}".center(width))
    print("=" * width)


def run_pipeline() -> bool:
    print_banner("INCUBRIX VISIBILITY ENGINE: PHASE 1 RESEARCH PIPELINE")
    print("Starting automated execution of Phase 1 research and question discovery...\n")

    # 1. Product Observations
    print("[1/5] Exporting 5 evidence-backed product observations...")
    obs_path = export_product_observations("data/research/product_observations.csv")
    obs_list = get_product_observations()
    print(f"      -> Successfully saved {len(obs_list)} observations to {obs_path}")

    # 2. Strategic Growth Opportunities
    print("[2/5] Exporting 3 prioritized search & AI visibility opportunities...")
    opp_path = export_growth_opportunities("data/research/opportunities.csv")
    opp_list = get_growth_opportunities()
    print(f"      -> Successfully saved {len(opp_list)} opportunities to {opp_path}")

    # 3. Source Register
    print("[3/5] Exporting research source register...")
    src_path = export_source_register_csv("data/research/source_register.csv")
    src_list = get_source_register()
    print(f"      -> Successfully saved {len(src_list)} sources to {src_path}")

    # 4. Question Collection & Deduplication
    print("[4/5] Ingesting and deduplicating 100-question baseline...")
    questions = get_verified_questions()
    df_raw = pd.DataFrame(questions)
    cleaned_df, dedup_report = deduplicate_dataset(df_raw)
    q_path = export_questions_csv("data/research/questions.csv")
    print(f"      -> Ingested: {dedup_report['total_records']} questions")
    print(f"      -> Exact duplicates detected: {dedup_report['exact_duplicates_count']}")
    print(f"      -> Near duplicates (threshold 0.85): {dedup_report['near_duplicates_count']}")
    print(f"      -> Successfully exported verified questions to {q_path}")

    # 5. Validation and Report Generation
    print("[5/5] Running schema, URL, date, category, and evidence validation...")
    val_report_path = generate_validation_report(cleaned_df, "outputs/validation_report.md")
    report = validate_questions_dataframe(cleaned_df)
    status = report["status_summary"]
    cat_dist = report["category_distribution"]
    deficient = report["deficient_categories"]

    print_banner("PHASE 1 RESEARCH VALIDATION SUMMARY")
    print(f"  Pipeline Overall Status : {'✅ PASSED' if report['is_valid'] else '❌ FAILED'}")
    print(f"  Verified Questions      : {status['verified']} / 100")
    print(f"  Pending Questions       : {status['pending']}")
    print(f"  Rejected Questions      : {status['rejected']}")
    print(f"  Exact Duplicates        : {status['exact_duplicates']}")
    print(f"  Near Duplicates         : {status['near_duplicates']}")
    print("-" * 75)
    print("  Category Distribution (10 Categories):")
    for cat, count in cat_dist.items():
        icon = "✅" if count >= 8 else "❌"
        print(f"    {icon} {cat:<35}: {count:>2} questions")
    print("-" * 75)
    if not deficient:
        print("  ✅ All 10 categories meet required sufficiency thresholds (zero deficiencies).")
    else:
        print(f"  ❌ Deficiencies detected in {len(deficient)} categories!")

    print(f"\n  Detailed Markdown report generated at: {val_report_path}")
    print_banner("PHASE 1 EXECUTION COMPLETE")
    return report["is_valid"]


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
