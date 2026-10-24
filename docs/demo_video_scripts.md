# IncuBrix Visibility Engine: Demonstration Video Scripts & Production Guides

> **IncuBrix 2027 Graduate Growth Engineer Assessment — Option 3**  
> *Complete Shot Lists, Timestamps, Spoken Voiceover, On-Screen Action Guides & Recording Checklists*

---

## Production Standard & Recording Guidelines

- **Resolution**: 1920x1080 (1080p Full HD) or 2560x1440 (2K) at 60 FPS.
- **Audio**: Crisp condenser microphone, no background hum, normalized to -14 LUFS.
- **Pacing**: Steady cursor movement, no erratic mouse shaking, smooth window transitions.
- **Integrity Policy**: Completely unedited single-take recordings per video or clean section transitions. Zero deceptive edits or fabricated live claims. Clearly state which data is live, manually collected, imported, or simulated.

---

# VIDEO A: PRODUCT WALKTHROUGH & STRATEGIC DASHBOARD
- **Maximum Duration**: 5 minutes (Target: 4 minutes 45 seconds).
- **Target Audience**: Growth Engineering Hiring Committee, IncuBrix Leadership, Strategy Evaluators.
- **Primary Tool**: Streamlit Intelligence Dashboard on `http://localhost:8502`.

### Detailed Shot List & Speaking Script

```
====================================================================================================
TIMESTAMPS    | ON-SCREEN DISPLAY (WHAT TO SHOW)     | SPOKEN SCRIPT (VOICEOVER DIALOGUE)
====================================================================================================
0:00 - 0:45   | Streamlit Dashboard - Page 1         | "Hello everyone. I am presenting the IncuBrix AEO,
(45 seconds)  | (Overview). Camera on Headline KPI   |  SEO, and GEO Automated Visibility Engine, built for
              | Cards (0.0% Organic, 62.0% AI        |  Option 3 of the 2027 Growth Engineer assessment.
              | Overviews, 25.0% Snippets, 0.0% AI   |  IncuBrix is developing the AI operating system for
              | Mentions). Mouse hovers over         |  the creator economy—unifying discovery, creation,
              | 'Strategic Diagnosis'.               |  repurposing, publishing, and learning.
              |                                      |  To scale organic acquisition, this engine measures,
              |                                      |  diagnoses, and optimizes IncuBrix's visibility across
              |                                      |  traditional Google Search and generative AI engines
              |                                      |  like ChatGPT, Gemini, Perplexity, and Claude."
----------------------------------------------------------------------------------------------------
0:45 - 1:30   | Page 1: Competitor SoV Table & Asset | "Our empirical baseline reveals what we call the
(45 seconds)  | Status. Scroll to OpusClip (47%) and |  IncuBrix Visibility Paradox: IncuBrix currently has
              | Descript (44%). Highlight Asset      |  0.0% organic search presence and 0.0% AI mentions.
              | counts: 100 questions, 20 fixes,     |  However, 62% of creator queries trigger Google AI
              | 10 pages, 30 citation targets.       |  Overviews, and 25% trigger Featured Snippets.
              |                                      |  Currently, the market is captured by OpusClip at
              |                                      |  47% share of voice and Descript at 44%.
              |                                      |  To solve this, our engine unifies 100 verified
              |                                      |  questions, 20 technical SEO fixes, 10 publish-ready
              |                                      |  pages, and 30 citation opportunities into an
              |                                      |  automated execution pipeline."
----------------------------------------------------------------------------------------------------
1:30 - 2:15   | Switch to Page 2 (Questions          | "Navigating to Page 2, we see the inventory of 100
(45 seconds)  | Inventory). Filter by Category:      |  real, sourced creator questions. These are not
              | 'Content Repurposing'. Filter by     |  synthetic queries—they were collected from Google PAA,
              | Source Type: 'Community Discussion'. |  Reddit, and YouTube across 10 operational categories.
              | Click on Q001: Can AI generate full  |  Each record includes verified search intent, target
              | YouTube video scripts from a title?  |  audience, and relevance to IncuBrix's core product.
              |                                      |  Notice how filtering dynamically narrows the view,
              |                                      |  allowing growth teams to prioritize commercial intent."
----------------------------------------------------------------------------------------------------
2:15 - 3:00   | Switch to Page 3 (Search Visibility) | "On Page 3 and Page 4, we examine our search and AI
(45 seconds)  | and Page 4 (AI Assistant Visibility).|  visibility baseline. Across 200 Google checks in the
              | Show the SERP feature breakdown and  |  US, UK, and India over two days, we recorded 0 Google
              | the head-to-head AI assistant        |  rankings in the top 100.
              | mention cards (all 0 / 100).         |  Across 400 AI checks in ChatGPT, Gemini, Perplexity,
              | Show Perplexity citations table.     |  and Claude, IncuBrix received zero mentions and zero
              |                                      |  citations. Every single observation is backed by raw
              |                                      |  JSON responses with cryptographic hashes in the repo."
----------------------------------------------------------------------------------------------------
3:00 - 3:45   | Switch to Page 6 (Technical SEO      | "Page 6 displays our remediation plan: 20 prioritized
(45 seconds)  | Audit). Select FIX-01 (Schema JSON-LD)|  technical fixes. When we select FIX-01, the viewer
              | from the dropdown. Show formatted    |  instantly displays the ready-to-paste JSON-LD script
              | code artifact. Switch to Page 7      |  for SoftwareApplication schema.
              | (Content Pages). Select P01. Expand  |  Moving to Page 7, we see our 10 publish-ready pages.
              | markdown preview showing direct      |  Expanding Page P01, notice the Answer-First format:
              | answer in the first two sentences.   |  the direct, complete answer is delivered in the first
              |                                      |  two sentences, followed by structured steps and schema."
----------------------------------------------------------------------------------------------------
3:45 - 4:45   | Switch to Page 10 (Reports & Exports)| "Finally, Page 10 brings everything together for
(60 seconds)  | Click 'Generate Fresh Weekly Report' |  weekly reporting and exports. With a single click,
              | Show generated report text. Click    |  the engine generates an executive weekly report in
              | 'Download Visibility Baseline'.      |  markdown and JSON, detailing coverage, competitor
              | Show downloaded data/visibility.csv. |  shifts, and next actions.
              | Return to Page 1. Concluding words.  |  We can also generate structured editorial briefs for
              |                                      |  any question, or download our evidence-backed CSVs.
              |                                      |  This engine provides IncuBrix with a repeatable,
              |                                      |  defensible growth OS. Thank you."
====================================================================================================
```

---

# VIDEO B: TECHNICAL DEMONSTRATION & REPRODUCIBILITY PROOF
- **Maximum Duration**: 8 minutes (Target: 7 minutes 30 seconds).
- **Target Audience**: Technical Evaluators, Lead Software Engineers, Assessment Reviewers.
- **Primary Tools**: Terminal (iTerm2/VS Code), Python CLI (`run_engine.py`), SQLite Inspector, Pytest.

### Detailed Shot List & Speaking Script

```
====================================================================================================
TIMESTAMPS    | ON-SCREEN DISPLAY (TERMINAL COMMANDS)| SPOKEN SCRIPT (TECHNICAL VOICEOVER)
====================================================================================================
0:00 - 1:00   | Terminal open at repository root.    | "Welcome to the technical architecture demonstration
(60 seconds)  | Show git status (clean).             |  of the IncuBrix Automated Visibility Engine.
              | Display virtual environment info:    |  In this video, I will prove that another engineer
              | `which python` -> .venv/bin/python   |  can install, run, refresh, test, and recover the
              | `python --version` -> Python 3.14.5  |  system using simple, documented commands.
              | Display `requirements.txt`.          |  Our stack is clean: standard Python, SQLite, pandas,
              | Type: `python run_engine.py --help`  |  openpyxl, Streamlit, and pytest. No proprietary
              | Show unified CLI command list.       |  binary dependencies or unverified frameworks."
----------------------------------------------------------------------------------------------------
1:00 - 2:00   | Run: `python run_engine.py status`   | "Let's inspect the system status. Running 'status'
(60 seconds)  | Terminal displays 13 table counts:   |  queries data/visibility.db. Notice our 13 relational
              | - visibility_observations: 200       |  tables: 100 questions, 200 observations across Days 1
              | - raw_provider_responses: 1000       |  and 2, 1,000 immutable raw responses, 20 technical
              | - questions: 100                     |  fixes, 10 content pages, and 30 citation targets.
              | - recommended_fixes: 20              |  Now, let's run 'sync-all'. This demonstrates our
              | Type: `python run_engine.py sync-all`|  idempotent ingestion pipeline, ensuring data from
              | Terminal outputs sync confirmation.  |  Phases 1 to 5 synchronizes cleanly without duplicates."
----------------------------------------------------------------------------------------------------
2:00 - 3:00   | Run: `python run_engine.py metrics`  | "Next, we calculate our baseline visibility metrics.
(60 seconds)  | Terminal outputs exact formulas:     |  The output confirms: Organic Visibility is 0.0%, AI
              | - Organic Visibility: 0.0%           |  Overviews appear in 62.0% of queries, Featured
              | - AI Overviews: 62.0%                |  Snippets appear in 25.0%, and AI mentions are 0.0%.
              | - Snippets: 25.0%                    |  Notice our competitor Share of Voice ranking:
              | - Competitor SoV: OpusClip 47%, etc. |  OpusClip leads at 47%, followed by Descript at 44%.
              | Type: `python run_engine.py export-  |  Running 'export-visibility' generates our official
              | visibility` -> data/visibility.csv.  |  workbook-compatible 20-column visibility.csv."
----------------------------------------------------------------------------------------------------
3:00 - 4:15   | Run: `python run_engine.py refresh   | "Now, let's test a refresh cycle with new input.
(75 seconds)  | --scope UK`                          |  We execute 'refresh --scope UK'. The scheduler
              | Terminal displays:                   |  assigns a unique run ID, evaluates the 100 questions
              | - Run ID: RUN-...-UK                 |  against the UK market, logs execution telemetry, and
              | - Status: COMPLETED                  |  evaluates whether any visibility changes occurred.
              | Show SQLite query:                   |  Crucially, earlier Day 1 and Day 2 baseline records
              | `sqlite3 data/visibility.db "SELECT  |  are never overwritten; historical observations remain
              | count(*) FROM collection_runs;"`     |  completely preserved for longitudinal analysis."
----------------------------------------------------------------------------------------------------
4:15 - 5:30   | Failure Recovery Demonstration:      | "Now we demonstrate recovery from a simple failure.
(75 seconds)  | Run python snippet to simulate       |  In this test, we simulate an external provider
              | timeout error during collection:     |  timeout—such as Perplexity returning an HTTP 504.
              | `python -c "from src.engine.database |  The engine logs this event into our collection_errors
              | import EngineDatabase; ..."`         |  telemetry table with timestamp and error details.
              | Query `collection_errors` table:     |  Notice the critical safety principle: the engine does
              | Show logged error row. Verify that   |  NOT fabricate an observation or crash the run.
              | unaffected records remain usable.    |  Unaffected records remain completely intact."
----------------------------------------------------------------------------------------------------
5:30 - 6:30   | Automated Test Suite Execution:      | "To verify total system reliability, we execute the
(60 seconds)  | Run: `pytest -v`                     |  entire test suite across all phases.
              | Watch all 103 tests execute:         |  Notice the test suite:
              | - test_research.py (19 passed)       |  - 19 Phase 1 product and question tests
              | - test_visibility.py (21 passed)     |  - 21 Phase 2 baseline measurement tests
              | - test_seo_audit.py (15 passed)      |  - 15 Phase 3 technical SEO fix tests
              | - test_content.py (15 passed)        |  - 15 Phase 4 content validation tests
              | - test_citations.py (11 passed)      |  - 11 Phase 5 digital PR citation tests
              | - test_engine.py (15 passed)         |  - 15 Phase 6 automated engine tests
              | - test_submission.py (7 passed)      |  - 7 Phase 7 end-to-end and audit tests
              | Result: 103 passed in 2.14s.         |  All 103 tests pass cleanly in under 3 seconds."
----------------------------------------------------------------------------------------------------
6:30 - 7:30   | Inspect Submission Workbook:         | "Finally, let's verify our official submission
(60 seconds)  | Run python script to inspect tabs:   |  workbook. Tab 03_ENGINE_LAUNCH contains all engine
              | 01_INSIGHT, 02_QUESTIONS, 02b_FIXES, |  proofs and 90-day launch summary.
              | 02c_PAGES_CITATIONS, 03_ENGINE_LAUNCH|  Tab 04_SELF_CHECK shows that all minimum requirements
              | and 04_SELF_CHECK.                   |  are MET: 100 questions, 4 assistants, 2 days, 20
              | Show all self-check statuses: 'MET'. |  fixes, 10 pages, 30 targets, and tracker reruns.
              | Concluding remarks.                  |  The engine is fully reproducible, verifiable, and
              |                                      |  ready for evaluation. Thank you."
====================================================================================================
```

---

## Recording Checklist & Verification Standards

- [x] **Clean Terminal**: Clear all previous terminal buffer before starting recording (`clear`).
- [x] **Font Readability**: Terminal font set to Menlo/Monaco 16pt+ for high contrast and readability.
- [x] **Browser Zoom**: Streamlit dashboard set to 100% or 110% zoom for crisp typography.
- [x] **No Notifications**: Do Not Disturb enabled on macOS to eliminate notification popups.
- [x] **Honest Data Labelling**:
  - Phase 1 & 2 baseline data is labelled as **Genuine Empirical Baseline** ($N=100$ questions, $N=200$ SERP checks, $N=400$ AI checks).
  - Scope refresh runs are labelled as **Incremental Refresh Cycles** under unique `RUN-...` timestamps.
  - Failure recovery simulations are explicitly labelled as **Simulated Telemetry Error Checks**.
