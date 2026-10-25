# IncuBrix Analytic Engine: AEO, SEO & GEO Visibility Engine

> **IncuBrix 2027 Graduate Growth Engineer Assessment — Option 3**  
> *Developed by an MCA Graduate Engineer candidate. Production-grade data research, measurement, automation, and validation platform.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://incubrix-analytic-engine-ss.streamlit.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-SRIRAM--20SS%2Fincubrix--analytic--engine-blue?logo=github)](https://github.com/SRIRAM-20SS/incubrix-analytic-engine)
[![Tests Passing](https://img.shields.io/badge/pytest-103%20passed-brightgreen)](tests/)
[![Live Web URL](https://img.shields.io/badge/Web%20App-Online-emerald)](https://incubrix-analytic-engine-ss.streamlit.app)

**🌐 Live Production Web Application:** [https://incubrix-analytic-engine-ss.streamlit.app](https://incubrix-analytic-engine-ss.streamlit.app)  
**📦 GitHub Master Repository:** [https://github.com/SRIRAM-20SS/incubrix-analytic-engine](https://github.com/SRIRAM-20SS/incubrix-analytic-engine)

---

## 1. Project Overview & Architectural Vision

IncuBrix is building the AI-powered operating system for the creator economy, unifying the five stages of content workflow into a single live CreatorOps platform:
$$\text{Discover} \longrightarrow \text{Create} \longrightarrow \text{Repurpose} \longrightarrow \text{Publish} \longrightarrow \text{Learn}$$

This repository integrates all work from **Phases 1 through 6** into an enterprise-grade, automated Visibility Engine designed to measure, defend, and expand IncuBrix's presence across Answer Engine Optimization (**AEO**), Search Engine Optimization (**SEO**), and Generative Engine Optimization (**GEO**).

### Completed Pipeline Phases
- **Phase 1: Product Research & Question Discovery**: Live product audit, 5 observations, 3 growth opportunities, source register, and 100 verified creator questions across 10 operational categories.
- **Phase 2: SEO, AEO & GEO Visibility Baseline**: Empirical measurement across Google Search and 4 frontier AI models (**ChatGPT**, **Gemini**, **Perplexity**, **Claude**) on two distinct days across 3 markets (**US**, **UK**, **IN**), backed by SQLite relational persistence and workbook-compatible [`data/visibility.csv`](file:///Users/sriram/INCUBRIX%20ANALYTIC%20ENGINE/data/visibility.csv).
- **Phase 3: Technical SEO Audit & 20 Validated Fixes**: Deep inspection of `incubrix.com`, delivering 20 prioritized, actionable technical fixes with ready-to-paste code artifacts (`JSON-LD`, `llms.txt`, `robots.txt`, sitemaps, semantic tags) and automated syntax validators.
- **Phase 4: Publish-Ready SEO, AEO & GEO Content Pages**: 10 comprehensive, original pages (>14,200 total words, avg 1,425 words/page) built on Answer-First architecture with validated Schema.org structured data, verified sources, and internal link routing.
- **Phase 5: Third-Party Citation Opportunity Research**: 30 high-authority citation targets identified from Google SERP and Perplexity citations with ethical PR action angles and direct-answer placement strategies.
- **Phase 6: Automated Visibility Engine Architecture**: Full data ingestion pipeline into a 13-table SQLite database, standardized metrics engine, multi-provider adapters, 10-page interactive Streamlit dashboard, automated weekly executive reports, structured content brief generator, and a unified CLI orchestrator (`run_engine.py`).
- **Phase 7: Final Testing, Submission & 90-Day Launch Kit**: 100% reproducible evidence audit, comprehensive 13-week operational roadmap, demonstration video scripts, completed workbook with verified self-check (`MET`), and 103 automated verification tests.

---

## 2. Master Repository Directory Structure

```
INCUBRIX ANALYTIC ENGINE/
├── data/
│   ├── research/
│   │   ├── questions.csv               # Phase 1: 100 verified questions (15 fields)
│   │   ├── product_observations.csv    # Phase 1: 5 evidence-backed product observations
│   │   ├── opportunities.csv           # Phase 1: 3 prioritized growth opportunities
│   │   └── source_register.csv         # Phase 1: 5 verified sources with proof standards
│   ├── visibility.db                   # SQLite database (13 master relational tables)
│   └── visibility.csv                  # 100-row workbook-compatible baseline export
├── evidence/
│   └── raw/                            # 100 raw JSON files: q001_answers.json ... q100_answers.json
├── docs/
│   ├── research_methodology.md         # Phase 1: Provenance taxonomy & validation framework
│   ├── visibility_baseline_methodology.md # Phase 2: Metric formulas, adapter design & proof
│   ├── technical_seo_audit.md          # Phase 3: Comprehensive 20-fix technical audit report
│   ├── citation_research_report.md     # Phase 5: 30-target digital PR citation report
│   ├── reproducibility_audit.md        # Phase 7: 20-sample evidence reproducibility audit
│   ├── 90_day_launch_kit.md            # Phase 7: 13-week operational growth roadmap
│   ├── demo_video_scripts.md           # Phase 7: Video A & B shot lists and voiceover scripts
│   └── final_handover_report.md        # Phase 7: Master final assessment handover document
├── outputs/
│   ├── validation_report.md            # Phase 1: Schema, URL, and category validation report
│   ├── visibility_summary.md           # Phase 2: Baseline KPIs, 2-day variance & provider health
│   ├── competitor_analysis.md          # Phase 2: Competitor share of voice & displacement strategy
│   ├── fixes/
│   │   ├── fixes.csv                   # Phase 3: 20 technical fixes register
│   │   └── artifacts/                  # Phase 3: Ready-to-paste code artifacts (FIX-01 to FIX-20)
│   ├── pages/
│   │   ├── content_register.csv        # Phase 4: 10 content pages register
│   │   └── *.md                        # Phase 4: 10 complete publish-ready markdown pages
│   ├── citations/
│   │   └── citation_targets.csv        # Phase 5: 30 prioritized third-party citation targets
│   ├── briefs/
│   │   ├── brief_q001.md               # Phase 6: Automated structured content brief for Q001
│   │   └── brief_q021.md               # Phase 6: Automated structured content brief for Q021
│   └── reports/
│       ├── weekly_report_2026-10-24.md # Phase 6: Executive weekly report (Markdown)
│       └── weekly_report_2026-10-24.json # Phase 6: Executive weekly report (JSON)
├── reference/                          # Official assessment specs, briefing & Excel workbook
│   ├── IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO.pdf
│   ├── IncuBrixPSG2027GraduateBriefingOct2026pptx.pdf
│   └── IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx
├── submission/                         # Submission item 1: Completed workbook & mirrored outputs
│   ├── IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx
│   ├── citation_targets.csv            # 30 prioritized third-party citation targets
│   ├── fixes/                          # Mirrored 20 technical fix code artifacts
│   ├── content/                        # Mirrored 10 publish-ready markdown pages
│   └── screenshots/                    # Dashboard UI and audit verification screenshots
├── visibility/                         # Submission item 2: Main output directory (as per spec)
│   ├── visibility.csv                  # 100-row workbook-compatible baseline export
│   ├── raw_answers/                    # 100 raw JSON files with provider responses
│   ├── screenshots/                    # Verification screenshots
│   ├── fixes/                          # 20 technical fixes with code artifacts + audit report
│   ├── pages/                          # 10 publish-ready markdown pages + content register
│   └── citation_plan.csv               # 30 prioritized third-party citation targets
├── src/
│   ├── research/                       # Phase 1: Sourcing, deduplication & validation
│   ├── visibility/                     # Phase 2: Baseline collection & adapters
│   ├── seo_audit/                      # Phase 3: Technical audit & validators
│   ├── content/                        # Phase 4: Page builder & QA validators
│   ├── citations/                      # Phase 5: PR targets & ethical pitch engines
│   └── engine/                         # Phase 6: Core Automation Engine
│       ├── database.py                 # SQLite manager for all 13 unified tables
│       ├── ingestion.py                # Idempotent sync of Phase 1-5 artifacts into SQLite
│       ├── metrics.py                  # Formulas, denominators, coverage & SoV calculations
│       ├── weekly_reporter.py          # Executive weekly report generator (MD + JSON)
│       ├── brief_generator.py          # On-demand structured editorial content briefs
│       └── scheduler.py                # Refresh workflow, run history & delta alerts
├── tests/
│   ├── test_research.py                # Phase 1: 19 unit tests
│   ├── test_visibility.py              # Phase 2: 21 unit tests
│   ├── test_seo_audit.py               # Phase 3: 15 unit tests
│   ├── test_content.py                 # Phase 4: 15 unit tests
│   ├── test_citations.py               # Phase 5: 11 unit tests
│   ├── test_engine.py                  # Phase 6: 15 unit tests
│   └── test_submission.py              # Phase 7: 7 integration tests (Total: 103 passing tests)
├── app.py                              # Phase 6: 10-page interactive Streamlit dashboard
├── run_engine.py                       # Phase 6: Unified CLI orchestrator
└── requirements.txt                    # Project dependencies
```

---

## 3. Database Architecture (All 13 SQLite Tables)

The engine persists all observations, entities, and outputs in [`data/visibility.db`](file:///Users/sriram/INCUBRIX%20ANALYTIC%20ENGINE/data/visibility.db), strictly enforcing primary keys, timestamps, and relational integrity across 13 tables:

| # | Table Name | Description | Key Columns |
|---|------------|-------------|-------------|
| 1 | `collection_runs` | Collection execution history and telemetry | `run_id`, `run_type`, `started_at`, `status` |
| 2 | `visibility_observations` | Day 1 & Day 2 Google SERP & AI measurements | `observation_id`, `question_id`, `day_number`, `google_position` |
| 3 | `raw_provider_responses` | Full raw responses with SHA-256 integrity hashes | `response_id`, `question_id`, `provider`, `raw_response_text` |
| 4 | `citations` | Sourced URLs cited by Google SERP and Perplexity | `citation_id`, `question_id`, `cited_url`, `anchor_text` |
| 5 | `competitor_mentions` | Named competitor mentions by provider | `mention_id`, `question_id`, `competitor_name`, `provider` |
| 6 | `collection_errors` | Telemetry logs for timeout/rate-limit errors | `error_id`, `run_id`, `provider`, `error_details` |
| 7 | `questions` | Master repository of 100 creator questions | `question_id`, `question_text`, `category`, `search_intent` |
| 8 | `sources` | Sourced platforms and proof standards | `source_id`, `source_name`, `access_method`, `question_count` |
| 9 | `audit_findings` | Issues identified during site inspection | `finding_id`, `category`, `severity`, `affected_url` |
| 10 | `recommended_fixes` | 20 prioritized technical SEO fixes | `fix_id`, `priority`, `recommended_solution`, `file_artifact` |
| 11 | `content_pages` | 10 publish-ready AEO/GEO content pages | `page_id`, `seo_title`, `target_question_id`, `word_count` |
| 12 | `citation_opportunities`| 30 prioritized third-party PR targets | `target_id`, `priority`, `target_url`, `suggested_ethical_action` |
| 13 | `validation_results` | Automated QA test and compliance records | `validation_id`, `validation_type`, `status`, `issues_detected` |

---

## 4. Unified CLI Orchestrator (`run_engine.py`)

The engine provides a single executable command-line interface for all data pipelines, reports, and administrative tasks:

```bash
# View all available CLI commands
./.venv/bin/python run_engine.py --help

# 1. Check system status, database table row counts, and headline metrics
./.venv/bin/python run_engine.py status

# 2. Synchronize all Phase 1-5 artifacts idempotently into SQLite
./.venv/bin/python run_engine.py sync-all

# 3. Calculate and display standardized visibility metrics and competitor SoV
./.venv/bin/python run_engine.py metrics

# 4. Generate executive weekly visibility reports (Markdown & JSON)
./.venv/bin/python run_engine.py report

# 5. Generate a structured editorial content brief for any question
./.venv/bin/python run_engine.py brief --question-id Q001

# 6. Execute a collection refresh cycle with change-detection alerts
./.venv/bin/python run_engine.py refresh --scope UK

# 7. Export workbook-compatible visibility.csv (100 rows, 20 columns)
./.venv/bin/python run_engine.py export-visibility

# 8. Launch the 10-page Streamlit Dashboard on port 8502
./.venv/bin/python run_engine.py dashboard --port 8502

# 9. Run the entire automated test suite (96 tests)
./.venv/bin/python run_engine.py test
```

---

## 5. Interactive Streamlit Dashboard (10 Pages)

Launch the dashboard locally via:
```bash
./.venv/bin/streamlit run app.py --server.port 8502 --server.headless true
```
Open **`http://localhost:8502`** in your browser. The dashboard contains 10 dedicated intelligence pages:

1. **Overview**: 6 headline KPI cards, The IncuBrix Visibility Paradox diagnosis, competitor Share of Voice table, and asset delivery counts.
2. **Questions Inventory**: Searchable and filterable table of all 100 questions with Category, Source Type, and text filters.
3. **Search Visibility**: Detailed Google SERP features (AI Overviews, Featured Snippets, People Also Ask) with direct observation logs.
4. **AI Assistant Visibility**: Head-to-head mention and citation rates across ChatGPT, Gemini, Perplexity, and Claude with competitor co-occurrence tables.
5. **Trends & Markets**: Day 1 vs. Day 2 temporal stability analysis (100.0% stability) and multi-market breakdown (US, UK, IN).
6. **Technical SEO Audit**: Complete register of 20 prioritized fixes with an interactive code viewer for ready-to-paste artifacts (`JSON-LD`, `llms.txt`, `robots.txt`).
7. **Content Pages**: 10 publish-ready pages with Answer-First verification and an interactive markdown preview expander.
8. **Citation Targets**: 30 prioritized third-party targets with publisher authority, page type, and ethical action angles.
9. **Collection Runs**: Execution telemetry, timestamp logging, check counts, and system status across all refresh cycles.
10. **Reports & Exports**: Integrated tabs to trigger fresh weekly reports, generate on-demand editorial content briefs, and download all CSV registers directly.

---

## 6. Empirical Visibility Baseline & Standardized Formulas

All metrics are calculated with explicit denominators, distinct separation of mentions from citations, and zero fabricated numbers:

$$\text{Organic Visibility Score} = \frac{\text{Queries with IncuBrix in Top 100}}{\text{Total Evaluated Queries}} = \frac{0}{100} = \mathbf{0.0\%}$$

$$\text{AI Overview Presence Rate} = \frac{\text{Queries Triggering Google AI Overview}}{\text{Total Evaluated Queries}} = \frac{62}{100} = \mathbf{62.0\%}$$

$$\text{Featured Snippet Presence Rate} = \frac{\text{Queries Triggering Featured Snippets}}{\text{Total Evaluated Queries}} = \frac{25}{100} = \mathbf{25.0\%}$$

$$\text{People Also Ask Presence Rate} = \frac{\text{Queries Triggering PAA Boxes}}{\text{Total Evaluated Queries}} = \frac{16}{100} = \mathbf{16.0\%}$$

$$\text{AI Assistant Mention Rate} = \frac{\text{AI Checks Outputting 'IncuBrix' Token}}{\text{Total AI Checks (100 Questions} \times \text{4 Assistants)}} = \frac{0}{400} = \mathbf{0.0\%}$$

$$\text{AI Assistant Citation Rate} = \frac{\text{AI Checks Providing a Hyperlink to incubrix.com}}{\text{Total AI Checks (100 Questions} \times \text{4 Assistants)}} = \frac{0}{400} = \mathbf{0.0\%}$$

$$\text{Two-Day Stability Rate} = \frac{\text{Queries with Unchanged Features on Day 2}}{\text{Total Evaluated Queries}} = \frac{100}{100} = \mathbf{100.0\%}$$

### Top Competitors Share of Voice (Empirical Baseline)
- **OpusClip**: 47 questions (47.0% SoV) — Dominates video repurposing & captioning.
- **Descript**: 44 questions (44.0% SoV) — Dominates audio/video text-based editing.
- **CapCut**: 21 questions (21.0% SoV) — Dominates mobile editing & viral templates.
- **Veed.io**: 19 questions (19.0% SoV) — Dominates browser-based subtitle workflows.
- **Munch**: 13 questions (13.0% SoV) — Dominates automated clip extraction.

---

## 7. Automated Verification Suite (103 Tests Passing)

The codebase includes 103 comprehensive, automated pytest unit and integration tests across 7 dedicated test modules:

```bash
# Run the entire test suite
./.venv/bin/pytest -v
```

### Test Suite Breakdown:
- **`tests/test_research.py` (19 tests)**: Schema compliance, non-empty cells, category distribution, valid URLs, valid dates, text normalizer, and Jaccard near-duplicate detector.
- **`tests/test_visibility.py` (21 tests)**: SQLite schema integrity, two-day observation preservation, mention vs citation separation, competitor extraction, and CSV export compliance.
- **`tests/test_seo_audit.py` (15 tests)**: 20 fixes existence, JSON-LD schema validity, XML sitemap structure, `llms.txt` format, and workbook tab `02b_FIXES` sync.
- **`tests/test_content.py` (15 tests)**: Word counts (>800 words), direct-answer placement in first two sentences, JSON-LD parse test, superlative blocker, and workbook tab `02c_PAGES_CITATIONS` sync.
- **`tests/test_citations.py` (11 tests)**: 30 citation targets existence, high/medium/low priority balance, ethical action verification, and workbook tab `02c_PAGES_CITATIONS` sync.
- **`tests/test_engine.py` (15 tests)**: All 13 SQLite tables validation, historical record preservation, formula verification, weekly report generation, content brief generation, and scheduler refresh cycles.
- **`tests/test_submission.py` (7 tests)**: Phase 7 Normal Run (Test A), Refresh with New Input (Test B), Simple Failure Recovery (Test C), 20-sample Reproducibility Audit (Test D), and Workbook Self-Check formula integrity (Test E).

---

## 8. Technical Interview Guide (For MCA Candidate Defense)

When defending this architecture in a technical interview with senior engineering leadership, articulate these core design decisions:

1. **Relational Normalization vs. Monolithic Strings**:
   - *"Rather than storing LLM responses and SERP observations as opaque, unsearchable markdown blobs, our engine structures data into 13 relational SQLite tables. This allows instant SQL queries for competitor co-occurrence, multi-market breakdowns, and period-over-period stability without reprocessing raw text."*
2. **Thread-Safe Read Pools in Streamlit**:
   - *"Streamlit executes reruns in separate worker threads. Passing a shared SQLite connection across threads triggers `sqlite3.ProgrammingError`. We resolved this by implementing thread-safe query helpers (`query_df`) using contextual connections and setting `check_same_thread=False` on the master engine connection, ensuring concurrent UI queries never block or corrupt the database."*
3. **Strict Separation of Mentions vs. Citations**:
   - *"In LLM visibility engineering, a brand mention and a brand citation are distinct events. A mention is a semantic namecheck within generative text; a citation is a hyperlinked attribution pointing to a canonical domain. Conflating the two produces misleading KPIs. Our adapters enforce distinct parsing rules for each."*
4. **Distinguishing Zero Visibility from Collection Failure**:
   - *"A major pitfall in growth data engineering is treating HTTP timeouts or API errors as zero-visibility scores. Our engine logs all network anomalies to `collection_errors` and verifies that 1,000 out of 1,000 checks completed successfully, proving IncuBrix's 0.0% visibility is an empirical reality, not a collection defect."*
5. **Idempotency & Historical Immutability**:
   - *"When running incremental refreshes, earlier observations are never overwritten. New collection runs receive unique `run_id` stamps and update the historical time-series, allowing accurate period-over-period delta detection."*
