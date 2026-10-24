"""
IncuBrix Automated Visibility Engine: CLI Orchestrator (Phase 6)
Unified Command-Line Interface providing full automation for:
- Data ingestion & synchronization
- Empirical metric calculation
- Visibility baseline exporting
- Weekly executive reporting
- Content brief generation
- Dashboard launching
- Automated test execution
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

from src.engine.database import EngineDatabase
from src.engine.ingestion import DataIngestor
from src.engine.metrics import EngineMetrics
from src.engine.weekly_reporter import WeeklyReporter
from src.engine.brief_generator import ContentBriefGenerator
from src.engine.scheduler import RefreshWorkflow


def cmd_status(args):
    print("\n" + "=" * 70)
    print("           INCUBRIX VISIBILITY ENGINE: SYSTEM STATUS")
    print("=" * 70)
    db = EngineDatabase()
    counts = db.get_table_counts()
    print("Database Tables & Row Counts (data/visibility.db):")
    for t, c in counts.items():
        print(f" - {t:<28}: {c:>5} records")

    em = EngineMetrics(db)
    m = em.get_summary_metrics()
    print("\nBaseline Visibility Metrics:")
    print(f" - Organic Visibility Score   : {m['organic_visibility_score']}%")
    print(f" - AI Overview Trigger Rate    : {m['ai_overview_presence_rate']}%")
    print(f" - Featured Snippet Rate       : {m['featured_snippet_rate']}%")
    print(f" - PAA Presence Rate           : {m['paa_presence_rate']}%")
    print(f" - AI Assistant Mention Rate   : {m['ai_assistant_mention_rate']}%")
    print(f" - Two-Day Stability Rate      : {m['two_day_stability_rate']}%")
    db.close()
    print("=" * 70 + "\n")


def cmd_sync_all(args):
    print("\nSynchronizing all Phase 1-5 data artifacts into SQLite database...")
    ingestor = DataIngestor()
    results = ingestor.sync_all()
    for k, v in results.items():
        print(f" -> {k}: {v}")
    ingestor.db.close()
    print("Sync completed successfully.\n")


def cmd_metrics(args):
    db = EngineDatabase()
    em = EngineMetrics(db)
    m = em.get_summary_metrics()
    print("\n" + "=" * 70)
    print("             INCUBRIX EMPIRICAL VISIBILITY METRICS")
    print("=" * 70)
    for k, v in m.items():
        if k == "top_competitors":
            print("\nTop Competitors Share of Voice:")
            for c in v:
                print(f"  * {c['name']:<12}: {c['questions_present']} questions ({c['share_of_voice_pct']}%)")
        else:
            print(f" - {k:<30}: {v}")
    db.close()
    print("=" * 70 + "\n")


def cmd_report(args):
    report_date = args.date or datetime.now().strftime("%Y-%m-%d")
    print(f"\nGenerating executive weekly report for date: {report_date}...")
    wr = WeeklyReporter()
    paths = wr.generate_report(report_date=report_date)
    print(f" -> Markdown Report: {paths['markdown_report']}")
    print(f" -> JSON Report:     {paths['json_report']}")
    wr.db.close()
    print("Weekly report generation complete.\n")


def cmd_brief(args):
    qid = args.question_id.upper()
    print(f"\nGenerating structured content brief for question {qid}...")
    cbg = ContentBriefGenerator()
    try:
        b = cbg.generate_brief_for_question(qid)
        print(f" -> Question: {b['primary_question']}")
        print(f" -> Title:    {b['proposed_title']}")
        print(f" -> Slug:     {b['proposed_slug']}")
        print(f" -> Saved to: {b['markdown_path']}")
    except KeyError as e:
        print(f"Error: {e}")
    finally:
        cbg.db.close()
    print("Brief generation complete.\n")


def cmd_refresh(args):
    scope = args.scope.upper()
    print(f"\nExecuting visibility collection refresh cycle (Scope: {scope})...")
    rw = RefreshWorkflow()
    res = rw.execute_refresh_cycle(scope=scope)
    print(f" -> Run ID:      {res['run_id']}")
    print(f" -> Status:      {res['status']}")
    print(f" -> Questions:   {res['questions_evaluated']}")
    print(f" -> Alerts:      {res['visibility_alerts_count']}")
    rw.db.close()
    print("Refresh cycle completed.\n")


def cmd_export_visibility(args):
    print("\nExporting workbook-compatible visibility.csv...")
    from src.visibility.baseline_exporter import export_visibility_csv
    out_path = export_visibility_csv()
    print(f" -> Exported 100-row baseline to: {out_path}\n")


def cmd_dashboard(args):
    port = args.port or 8503
    print(f"\nLaunching Streamlit Dashboard on port {port}...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", str(port), "--server.headless", "true"]
    subprocess.run(cmd)


def cmd_test(args):
    print("\nRunning full automated test suite across all phases...")
    cmd = [sys.executable, "-m", "pytest", "-v"]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="IncuBrix Automated Visibility Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available engine commands")

    # Status
    p_status = subparsers.add_parser("status", help="Display system status and table counts")
    p_status.set_defaults(func=cmd_status)

    # Sync All
    p_sync = subparsers.add_parser("sync-all", help="Synchronize all Phase 1-5 artifacts into SQLite")
    p_sync.set_defaults(func=cmd_sync_all)

    # Metrics
    p_metrics = subparsers.add_parser("metrics", help="Calculate and print visibility baseline metrics")
    p_metrics.set_defaults(func=cmd_metrics)

    # Report
    p_report = subparsers.add_parser("report", help="Generate executive weekly visibility report")
    p_report.add_argument("--date", help="Report date (YYYY-MM-DD)", default=None)
    p_report.set_defaults(func=cmd_report)

    # Brief
    p_brief = subparsers.add_parser("brief", help="Generate content brief for a specific question ID")
    p_brief.add_argument("--question-id", required=True, help="Question ID (e.g. Q021)")
    p_brief.set_defaults(func=cmd_brief)

    # Refresh
    p_refresh = subparsers.add_parser("refresh", help="Run a visibility collection refresh cycle")
    p_refresh.add_argument("--scope", default="ALL", choices=["ALL", "GOOGLE", "AI", "US", "UK", "IN"])
    p_refresh.set_defaults(func=cmd_refresh)

    # Export Visibility
    p_export = subparsers.add_parser("export-visibility", help="Export primary data/visibility.csv")
    p_export.set_defaults(func=cmd_export_visibility)

    # Dashboard
    p_dash = subparsers.add_parser("dashboard", help="Launch interactive Streamlit dashboard")
    p_dash.add_argument("--port", type=int, default=8503, help="Port to run Streamlit on")
    p_dash.set_defaults(func=cmd_dashboard)

    # Test
    p_test = subparsers.add_parser("test", help="Execute automated test suite across all phases")
    p_test.set_defaults(func=cmd_test)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
