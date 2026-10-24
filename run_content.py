"""
IncuBrix Visibility Engine: Phase 4 Content Generation Pipeline Runner
Executes automated generation of 10 publish-ready SEO, AEO & GEO content pages,
validates compliance with quality assurance standards, exports the content register CSV,
and populates tab 02c_PAGES_CITATIONS in the submission workbook.
"""

import os
import sys
from src.content.topic_selector import TopicSelector
from src.content.page_generator import PageGenerator
from src.content.publishing_validator import PublishingValidator


def main():
    print("\n" + "=" * 75)
    print("      INCUBRIX VISIBILITY ENGINE: PHASE 4 PUBLISH-READY PAGES ENGINE    ")
    print("=" * 75)
    print("Starting automated generation and validation of 10 publish-ready pages...\n")

    # Step 1: Topic selection
    print("[1/4] Selecting 10 prioritized topics from Phase 1 & 2 research...")
    topics = TopicSelector.get_all_topics()
    t_val = TopicSelector.validate_topic_mix()
    print(f"      -> Selected {len(topics)} topics across {t_val['content_types_count']} content formats")
    print(f"      -> Target Opportunities covered: {', '.join(t_val['opportunities_covered'])}")

    # Step 2: Page generation
    print("[2/4] Rendering 10 complete markdown pages with JSON-LD & verified links...")
    pages = PageGenerator.generate_all_pages(
        output_dir="outputs/pages",
        submission_dir="submission/content"
    )
    print(f"      -> 10 markdown pages written to outputs/pages/ (page_01.md ... page_10.md)")
    print(f"      -> 10 submission files written to submission/content/")

    # Step 3: Publishing Quality Validation
    print("[3/4] Running automated publishing quality validator across all 10 pages...")
    val_report = PublishingValidator.validate_all_pages("outputs/pages")
    print(f"      -> Validation Result: {val_report['valid_count']}/{val_report['pages_checked']} pages passed")
    if not val_report["all_valid"]:
        print("      [WARNING] Validation failures detected:")
        for r in val_report["results"]:
            if not r["is_valid"]:
                print(f"        - {os.path.basename(r['file_path'])}: {r['errors']}")
        sys.exit(1)
    else:
        print("      -> All 10 pages successfully validated (0 errors, >800 words each, valid JSON-LD)")

    # Step 4: Export Deliverables & Workbook Sync
    print("[4/4] Exporting content_register.csv and populating submission workbook...")
    csv_path = PageGenerator.export_content_register_csv(pages, "outputs/pages/content_register.csv")
    wb_path = PageGenerator.populate_workbook_tab_02c(
        pages,
        "submission/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx"
    )
    print(f"      -> Content Register CSV: {csv_path}")
    print(f"      -> Submission Workbook Updated: {wb_path} (Tab: 02c_PAGES_CITATIONS)")

    print("\n" + "=" * 75)
    print("                    PHASE 4 CONTENT SUMMARY DASHBOARD                   ")
    print("=" * 75)
    print(f"{'Page ID':<8} | {'Format':<22} | {'Words':<6} | {'Target Question':<32} | {'Status'}")
    print("-" * 75)
    for p in pages:
        t = p["topic"]
        idx_num = int(p["page_id"].replace("P", ""))
        fp = f"outputs/pages/page_{idx_num:02d}.md"
        res = PublishingValidator.validate_page_file(fp)
        q_trunc = (t["primary_question"][:29] + "...") if len(t["primary_question"]) > 32 else t["primary_question"]
        print(f"{p['page_id']:<8} | {t['content_type'][:22]:<22} | {res['word_count']:<6} | {q_trunc:<32} | ✅ Pass")
    print("-" * 75)
    print("All 10 pages ready for editorial review and direct deployment on incubrix.com.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
