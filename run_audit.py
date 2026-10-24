#!/usr/bin/env python3
"""
IncuBrix Analytic Engine: Phase 3 Technical SEO Audit & 20 Validated Fixes Pipeline
Executes the complete Phase 3 technical audit:
1. Audits live site crawlability, metadata, structured data, sitemaps, robots.txt, and llms.txt.
2. Validates all 20 code artifacts with independent syntax, schema, and XML validators.
3. Exports outputs/fixes/fixes.csv (20 prioritized fixes).
4. Generates comprehensive technical audit report at outputs/fixes/technical_audit.md.
5. Populates tab 02b_FIXES in the submission workbook.
"""

import sys
import os

from src.seo_audit.crawler import SiteCrawler
from src.seo_audit.validators import FixValidator
from src.seo_audit.fix_generator import (
    get_all_technical_fixes,
    export_fixes_csv,
    generate_technical_audit_report,
    populate_workbook_fixes
)


def print_banner(title: str):
    width = 75
    print("\n" + "=" * width)
    print(f" {title}".center(width))
    print("=" * width)


def run_pipeline() -> bool:
    print_banner("INCUBRIX VISIBILITY ENGINE: PHASE 3 TECHNICAL SEO AUDIT")
    print("Starting automated execution of website technical audit and 20 fixes...\n")

    # 1. Site Crawl & Live Audit
    print("[1/4] Inspecting public pages, robots.txt, sitemap.xml, and llms.txt...")
    crawler = SiteCrawler(base_url="https://incubrix.com", timeout=10)
    pages = crawler.crawl_core_pages()
    accessible_pages = sum(1 for p in pages if p["status_code"] == 200)
    print(f"      -> Successfully inspected {len(pages)} core routes ({accessible_pages} returning HTTP 200)")

    # 2. Validate All 20 Code Artifacts
    print("[2/4] Validating 20 ready-to-paste code artifacts with independent validators...")
    fixes = get_all_technical_fixes()
    validation_failures = 0

    for f in fixes:
        code = f.get("implementation_code", "")
        fn = os.path.basename(f.get("file_artifact", ""))
        val_res = FixValidator.validate_artifact(f["fix_id"], code, fn)
        if not val_res["is_valid"]:
            print(f"      ❌ {f['fix_id']} failed validation: {val_res['message']}")
            validation_failures += 1

    if validation_failures == 0:
        print(f"      -> All 20 code artifacts successfully validated (0 syntax/schema errors)")
    else:
        print(f"      ⚠️ {validation_failures} artifacts flagged validation issues!")

    # 3. Export Machine-Readable Fix Register & Report
    print("[3/4] Exporting fixes.csv and technical_audit.md...")
    csv_path = export_fixes_csv("outputs/fixes/fixes.csv")
    md_path = generate_technical_audit_report("outputs/fixes/technical_audit.md")
    print(f"      -> Fixes Register CSV: {csv_path}")
    print(f"      -> Technical Audit Markdown Report: {md_path}")

    # 4. Populate Submission Workbook
    print("[4/4] Populating tab 02b_FIXES in submission workbook...")
    wb_path = populate_workbook_fixes()
    if wb_path:
        print(f"      -> Updated submission workbook: {wb_path}")

    # Summary Dashboard
    print_banner("PHASE 3 TECHNICAL AUDIT SUMMARY DASHBOARD")
    print(f"  Total Technical Fixes Documented : {len(fixes)}")
    print(f"  Critical Priority Fixes          : {sum(1 for f in fixes if f['priority'] == 'Critical')}")
    print(f"  High Priority Fixes              : {sum(1 for f in fixes if f['priority'] == 'High')}")
    print(f"  Medium Priority Fixes            : {sum(1 for f in fixes if f['priority'] == 'Medium')}")
    print("-" * 75)
    print("  Category Breakdown:")
    cat_counts = {}
    for f in fixes:
        c = f["audit_category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {cat:<35}: {count:>2} fixes")
    print("-" * 75)
    print("  High-Impact Highlights Ready to Deploy:")
    print("    1. FIX-01 & FIX-08: Organization & SoftwareApplication JSON-LD schemas")
    print("    2. FIX-02 & FIX-20: llms.txt & llms-full.txt Generative Engine standard feeds")
    print("    3. FIX-03: FAQPage Rich Snippet schema on /faq")
    print("    4. FIX-04 & FIX-14: Sitemap <lastmod> timestamps & AI Crawler robots.txt rules")
    print("    5. FIX-05: Valid H1 headline replacing empty <h1> tag on /manifesto")
    print_banner("PHASE 3 EXECUTION COMPLETE")

    return validation_failures == 0


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
