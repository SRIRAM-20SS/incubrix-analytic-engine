# IncuBrix 90-Day Visibility & Growth Launch Kit (Weeks 1–13)

> **IncuBrix 2027 Graduate Growth Engineer Assessment — Option 3**  
> *Target Domain: incubrix.com | Operational Baseline: 0.0% Organic / 0.0% AI Mentions | Target: Capture First AEO/GEO Footprint*

---

## 1. Executive Roadmap Overview

This 90-day operational roadmap outlines the exact execution sequence to transition IncuBrix from an empirical zero-visibility baseline into an active, cited authority across Google Search, Google AI Overviews, Perplexity, ChatGPT, and Claude.

The plan is divided into three distinct 30-day phases across 13 operational weeks:

$$\begin{matrix}
\mathbf{Days\ 1-30:\ Foundation} & \longrightarrow & \mathbf{Days\ 31-60:\ Expansion} & \longrightarrow & \mathbf{Days\ 61-90:\ Optimization} \\
\text{Weeks 1–4} & & \text{Weeks 5–8} & & \text{Weeks 9–13} \\
\text{Deploy Technical Fixes} & & \text{Scale Content Hubs} & & \text{Refresh & Displace} \\
\text{Publish Initial 10 Pages} & & \text{Digital PR Outreach} & & \text{Conversion Attribution} \\
\text{Automate Tracking Engine} & & \text{Expand to 200 Queries} & & \text{Full Longitudinal Audit}
\end{matrix}$$

---

## 2. Resource & Budget Allocation ($349 / Month Operating Budget)

The launch kit operates on a lean, high-leverage growth stack requiring only **$349 per month** in tooling and API expenses:

| Tool / Service | Operational Responsibility | Monthly Cost | Rationale & Usage |
|---|---|:---:|---|
| **IncuBrix Visibility Engine** | Custom Python/SQLite 13-table tracker | **$0.00** | Proprietary engine running locally or via self-hosted VM |
| **Streamlit Community Cloud** | Stakeholder dashboard hosting | **$0.00** | Public or password-protected executive reporting dashboard |
| **Google Search Console / GA4** | Webmaster indexing & analytics | **$0.00** | Free native search indexing and click tracking |
| **Serper.dev API** | Automated Google SERP & feature tracking | **$50.00** | 50,000 queries/month for weekly multi-market checks (US, UK, IN) |
| **Frontier LLM API Credits** | OpenAI, Anthropic, Perplexity API | **$150.00** | Structured prompt evaluations across 100 questions weekly |
| **Ahrefs / Semrush Starter** | Keyword monitoring & backlink index | **$129.00** | Validates external link velocity and organic competitor rank |
| **Domain & DNS Hosting** | Cloudflare / Vercel Edge hosting | **$20.00** | Caching, security headers, and fast global delivery |
| **Total Monthly Operating Budget** | | **$349.00** | **Total 90-Day Tooling Budget: $1,047.00** |

---

## 3. Team Ownership Matrix (RACI)

- **GE**: Growth Engineer (Technical lead, engine automation, tracking)
- **CS**: Content Strategist (Answer-First writer, editorial briefs, fact-checking)
- **FED**: Frontend Developer (CMS integration, JSON-LD deployment, template styling)
- **PR**: Digital PR & Outreach Lead (Editorial pitches, citation placements, directories)

| Functional Responsibility | Growth Engineer (GE) | Content Strategist (CS) | Frontend Dev (FED) | Digital PR Lead (PR) |
|---|:---:|:---:|:---:|:---:|
| **Technical SEO Fixes (FIX-01 to FIX-20)** | **Accountable** | Informed | **Responsible** | Informed |
| **Content Creation & Editing (P01 to P10)** | Consulted | **Accountable** | Responsible | Informed |
| **AEO / Answer-First QA Validation** | Responsible | **Accountable** | Consulted | Informed |
| **Third-Party Citation Outreach (C01 to C30)** | Informed | Consulted | Informed | **Accountable** |
| **Engine Scheduler & Telemetry** | **Accountable** | Informed | Informed | Informed |
| **Weekly Visibility Reporting** | **Accountable** | Responsible | Informed | Responsible |

---

## 4. Stage 1: Days 1–30 — Technical Foundation & Core Footprint

### Week 1: Production Infrastructure & Priority 1 Technical Fixes
- **Objective**: Establish site crawlability, AI crawler access, and baseline analytics.
- **Specific Tasks**:
  1. Audit production deployment environment of `incubrix.com`.
  2. Implement `FIX-01` (`SoftwareApplication` JSON-LD) and `FIX-02` (`llms.txt`).
  3. Deploy `FIX-03` (`robots.txt` granting explicit access to GPTBot, PerplexityBot, ClaudeBot).
  4. Submit `FIX-04` (`sitemap.xml`) to Google Search Console.
  5. Connect automated tracking engine to production domain.
- **Deliverables**: Deployed `llms.txt`, updated `robots.txt`, validated XML sitemap, GSC verification.
- **Responsible Role**: Growth Engineer (Lead) & Frontend Dev.
- **Dependencies**: DNS and production code repo access from IncuBrix engineering.
- **Tools**: VS Code, Git, Google Search Console, Rich Results Test.
- **Estimated Budget**: $0 (Internal engineering).
- **KPI Target**: 100% crawlability score; 0 blocked crawlers; GSC sitemap status "Success".
- **Measurement Method**: GSC Coverage Report & Schema Markup Validator.
- **Risks & Mitigations**: Deployment delays on production CMS; fallback to edge injection via Cloudflare Workers.

### Week 2: Publishing Anchor Content Pages (P01 & P03)
- **Objective**: Deploy first high-intent answer pages targeting the largest video workflow gaps.
- **Specific Tasks**:
  1. Format and upload `P01` (Repurposing Long Videos into Shorts) and `P03` (Automated Video Podcast Workflow) into CMS.
  2. Embed validated `HowTo` and `FAQPage` Schema.org JSON-LD scripts.
  3. Verify Answer-First direct answers appear within the opening 50 words.
  4. Manually request Google indexing in Search Console.
- **Deliverables**: 2 live production pages on `incubrix.com` with validated schemas.
- **Responsible Role**: Content Strategist & Frontend Dev.
- **Dependencies**: Page design template approved; CMS publishing permissions.
- **Tools**: CMS (WordPress/Webflow/Next.js), Google Rich Results Test.
- **Estimated Budget**: $0.
- **KPI Target**: Direct indexing request submitted; 0 schema errors; word count > 1,400 words/page.
- **Measurement Method**: URL Inspection tool in GSC; Schema validator.
- **Risks & Mitigations**: Slow Google indexing; share pages across social channels to trigger crawler discovery.

### Week 3: Deploying Remaining Technical Fixes & Batch Publishing (P02, P04, P05)
- **Objective**: Remediate semantic HTML, canonical tags, and publish tool comparison hubs.
- **Specific Tasks**:
  1. Deploy `FIX-05` to `FIX-12` (canonical URLs, H1 headers, Open Graph tags, viewport tags).
  2. Publish `P02` (Best AI Video Editors 2026), `P04` (Auto Subtitles & Animated Captions), and `P05` (AI Video Scripts from Title).
  3. Establish internal linking network connecting P01-P05 to IncuBrix product features.
- **Deliverables**: 5 total live content pages; 12 technical fixes live in production.
- **Responsible Role**: Growth Engineer & Content Strategist.
- **Dependencies**: Week 2 indexing validation.
- **Tools**: CMS, Screaming Frog SEO Spider.
- **Estimated Budget**: $0.
- **KPI Target**: All 12 deployed fixes passing validation; internal link depth <= 2 clicks from homepage.
- **Measurement Method**: Full site crawl via Screaming Frog.
- **Risks & Mitigations**: Canonical loops; verify with automated unit tests before staging merge.

### Week 4: Publishing Pages P06–P10 & First Monthly Retrospective
- **Objective**: Complete initial 10-page content cluster and establish first 30-day baseline delta.
- **Specific Tasks**:
  1. Publish remaining 5 pages (`P06` through `P10`) targeting YouTube growth and multi-platform publishing.
  2. Execute full collection run using `python run_engine.py refresh --scope ALL`.
  3. Compile Month 1 Executive Report comparing initial Day 1/Day 2 baseline to current measurements.
  4. Verify that all 10 pages are cached and indexed.
- **Deliverables**: Complete 10-page hub live; Month 1 Visibility Report; 20 technical fixes completed.
- **Responsible Role**: Growth Engineer.
- **Dependencies**: All 10 pages QA-approved by Content Strategist.
- **Tools**: `run_engine.py`, Streamlit Dashboard, GSC.
- **Estimated Budget**: $50 (Serper API credits).
- **KPI Target**: 10/10 pages indexed; 20/20 technical fixes verified; first organic impressions registered in GSC.
- **Measurement Method**: GSC Performance Tab (Impressions > 100); `visibility.db` observation logs.
- **Risks & Mitigations**: New pages index slowly; build internal homepage links in site footer and navigation.

---

## 5. Stage 2: Days 31–60 — Content Expansion & Citation Seeding

### Week 5: Tier-1 Citation Outreach (Targets C01 to C10)
- **Objective**: Engage high-authority editorial comparison guides where competitors currently dominate citations.
- **Specific Tasks**:
  1. Conduct personalized outreach to editors of `C01` (Zapier), `C02` (Buffer), `C06` (TechRadar), and `C08` (G2).
  2. Pitch the "2026 AI Video Editing Latency & Accuracy Benchmark" data published on `P04`.
  3. Provide verified product screenshots and pricing details for IncuBrix inclusion.
- **Deliverables**: 10 personalized editorial pitches sent; tracking in PR pipeline CRM.
- **Responsible Role**: Digital PR Lead.
- **Dependencies**: Live `P04` benchmark page with verified methodology.
- **Tools**: Hunter.io, LinkedIn Outreach, Google Sheets PR Tracker.
- **Estimated Budget**: $50 (Outreach email software).
- **KPI Target**: 10 pitches delivered; >=3 editorial responses; >=1 confirmed listing update.
- **Measurement Method**: Email response rate; manual verification of target page revisions.
- **Risks & Mitigations**: Editors ignore unsolicited pitches; offer exclusive creator workflow data or co-marketing assets.

### Week 6: Community & Forum Answer Seeding (Targets C11 to C20)
- **Objective**: Establish authoritative presence on public creator discussion hubs (Reddit, Quora, Discord).
- **Specific Tasks**:
  1. Identify active creator questions on r/ContentCreators, r/YouTube, and r/VideoEditing matching Phase 1 questions.
  2. Provide comprehensive, educational direct answers solving specific workflow bottlenecks (e.g., audio silence removal, aspect ratio reframing).
  3. Transparently cite IncuBrix research and free workflow guides as supporting documentation.
- **Deliverables**: 15 helpful community answers posted adhering strictly to community guidelines (no spam).
- **Responsible Role**: Content Strategist & Growth Engineer.
- **Dependencies**: Aged Reddit/community accounts in good standing.
- **Tools**: Reddit, Quora, F5Bot (keyword alerts).
- **Estimated Budget**: $0.
- **KPI Target**: 15 answers posted; average upvote ratio > 80%; 0 moderator warnings or removals.
- **Measurement Method**: Reddit karma metrics; referral traffic in GA4.
- **Risks & Mitigations**: Account flagged for promotional posting; ensure 90% of answer value is self-contained educational advice without requiring a click.

### Week 7: Scaling Question Dataset from 100 to 200 Creator Queries
- **Objective**: Broaden the engine's query coverage to capture long-tail creator questions.
- **Specific Tasks**:
  1. Ingest 100 additional creator questions using `collect_questions.py` targeting YouTube Shorts, TikTok editing, and Instagram Reels workflows.
  2. Run deduplication engine (`deduplicate_questions.py`) to eliminate duplicates.
  3. Execute automated baseline checks across Google and 4 AI assistants for new queries.
  4. Generate content briefs for top 10 new commercial-intent queries using `run_engine.py brief`.
- **Deliverables**: Expanded dataset of 200 questions in `data/research/questions.csv`; 10 new content briefs.
- **Responsible Role**: Growth Engineer.
- **Dependencies**: Expanded Serper/LLM API budget.
- **Tools**: `run_engine.py`, SQLite database.
- **Estimated Budget**: $75 (API checks for 100 questions).
- **KPI Target**: 200 verified questions in database; 100% passing QA validation; 0 duplicates.
- **Measurement Method**: `pytest tests/test_engine.py`.
- **Risks & Mitigations**: Query cannibalization; cluster questions by semantic intent before content assignment.

### Week 8: Mid-Campaign Visibility Audit & Month 2 Retrospective
- **Objective**: Measure longitudinal visibility shifts and displacement of competitors.
- **Specific Tasks**:
  1. Execute bi-weekly automated visibility refresh (`python run_engine.py refresh --scope ALL`).
  2. Analyze changes in Featured Snippet capture rate and Google AI Overview trigger rate.
  3. Check Perplexity and ChatGPT for brand mentions or citations using automated regex scrapers.
  4. Produce Month 2 Executive Report with period-over-period variance charts.
- **Deliverables**: Month 2 Executive Report; delta alerts analysis; updated Streamlit dashboard.
- **Responsible Role**: Growth Engineer & Digital PR Lead.
- **Dependencies**: Weeks 5–7 completed actions.
- **Tools**: Streamlit Dashboard, `run_engine.py report`.
- **Estimated Budget**: $50.
- **KPI Target**: First 1–3 AI Overviews citing `incubrix.com`; Organic Visibility increases from 0.0% to >= 3.0%; at least 1 Tier-1 PR backlink acquired.
- **Measurement Method**: `visibility.db` metrics table; GSC Search Console performance data.
- **Risks & Mitigations**: Competitors expand content; prioritize Featured Snippet optimization on near-ranking queries.

---

## 6. Stage 3: Days 61–90 — Optimization, Conversion Attribution & Scaling

### Week 9: Featured Snippet & Answer-Box Optimization
- **Objective**: Optimize published pages that rank on Google page 2 (positions 11–20) into page 1 Featured Snippets.
- **Specific Tasks**:
  1. Inspect GSC query queries with high impressions but low click-through rates.
  2. Reformat direct-answer paragraphs into bulleted lists or 40–50 word definition summaries tailored for Google Snippets.
  3. Add HTML definition lists (`<dl>`, `<dt>`, `<dd>`) and table summaries.
- **Deliverables**: 5 updated content pages with refined Answer-First markup.
- **Responsible Role**: Content Strategist & Growth Engineer.
- **Dependencies**: GSC position data showing queries ranking in Top 30.
- **Tools**: GSC, Ahrefs, CMS.
- **Estimated Budget**: $0.
- **KPI Target**: Capture 2 Featured Snippets on Google US for high-value creator queries.
- **Measurement Method**: `visibility_observations` table; SERP scrapers.
- **Risks & Mitigations**: Snippet volatility; test variations on 2 pages before site-wide rollout.

### Week 10: Digital PR Second Wave (Software Directories & Resource Hubs)
- **Objective**: Secure verified listings on high-authority software directories (C21 to C30).
- **Specific Tasks**:
  1. Submit verified IncuBrix profiles to AlternativeTo, SaaSHub, ProductHunt, and Capterra.
  2. Ensure accurate product feature tagging (AI video repurposing, auto-captions, multi-platform publishing).
  3. Solicit genuine reviews from beta creators to build initial trust signals.
- **Deliverables**: 5 verified directory listings live with backlinks pointing to `incubrix.com`.
- **Responsible Role**: Digital PR Lead.
- **Dependencies**: Marketing collateral and verified product screenshots.
- **Tools**: Directory submission portals.
- **Estimated Budget**: $0 (Free verified profiles).
- **KPI Target**: 5 directory profiles active; domain authority growth in Ahrefs (+3 DR points).
- **Measurement Method**: Backlink verification via Ahrefs; referral tracking in GA4.
- **Risks & Mitigations**: Listing rejection; adhere strictly to submission guidelines without hyperbolic claims.

### Week 11: Generative Engine Optimization (GEO) Fine-Tuning
- **Objective**: Optimize content structure specifically for LLM retrieval-augmented generation (RAG) pipelines.
- **Specific Tasks**:
  1. Analyze raw responses from Perplexity and Gemini to identify which external sources are most frequently cited for creator queries.
  2. Synthesize key authoritative statistics and verifiable definitions onto `incubrix.com/research` hub.
  3. Expand `llms.txt` with deep links to newly created statistics and benchmark pages.
- **Deliverables**: Updated `llms.txt`; new `/research/creator-benchmarks-2026` landing page.
- **Responsible Role**: Growth Engineer & Frontend Dev.
- **Dependencies**: Perplexity citation analysis.
- **Tools**: Python analysis scripts, code editor.
- **Estimated Budget**: $0.
- **KPI Target**: Perplexity citation rate increases from 0.0% to >= 3.0% across evaluated queries.
- **Measurement Method**: Perplexity automated adapter query in `visibility_observations`.
- **Risks & Mitigations**: LLM citation lag; syndicating data via open PR channels speeds up RAG ingestion.

### Week 12: Conversion Funnel & Organic Sign-Up Attribution
- **Objective**: Connect visibility gains to creator sign-ups and product activations.
- **Specific Tasks**:
  1. Audit GA4 conversion events (`sign_up_start`, `sign_up_complete`, `export_completed`).
  2. Implement UTM parameters and contextual product call-to-actions (CTAs) within the 10 published pages.
  3. Measure conversion rate from organic visitors to free product trial users.
- **Deliverables**: GA4 attribution dashboard; optimized CTAs across all 10 pages.
- **Responsible Role**: Growth Engineer.
- **Dependencies**: IncuBrix product onboarding telemetry.
- **Tools**: GA4, Google Tag Manager.
- **Estimated Budget**: $0.
- **KPI Target**: Achieve >= 3.5% visitor-to-signup conversion rate on organic content pages.
- **Measurement Method**: GA4 Exploration reports; IncuBrix database user sign-ups.
- **Risks & Mitigations**: High bounce rate on informational pages; add interactive micro-tools or templates to boost engagement.

### Week 13: 90-Day Full Executive Review & Handover Presentation
- **Objective**: Final assessment of 90-day growth trajectory, ROI, and Phase 8 scaling recommendations.
- **Specific Tasks**:
  1. Run complete 90-day visibility audit comparing Day 0 baseline to Day 90 empirical data.
  2. Generate Final 90-Day Executive Report using `python run_engine.py report`.
  3. Deliver executive presentation to IncuBrix leadership with documented ROI, customer acquisition cost (CAC), and organic pipeline value.
  4. Hand over operational runbook and maintenance guides.
- **Deliverables**: 90-Day Executive Report; Handover Presentation Deck; Automated Maintenance Runbook.
- **Responsible Role**: Growth Engineer (Lead) & Leadership Team.
- **Dependencies**: All 12 prior weeks of telemetry and analytics.
- **Tools**: Slide deck, Streamlit Dashboard, `run_engine.py`.
- **Estimated Budget**: $0.
- **KPI Target**:
  - Organic Google Visibility: **5.0% to 10.0%** (from 0.0% baseline).
  - Google AI Overview Citations: **>= 5 queries citing IncuBrix**.
  - Perplexity / AI Citations: **>= 3 queries citing IncuBrix**.
  - Organic Impressions: **>= 15,000 monthly impressions**.
  - Organic Sign-ups: **>= 150 qualified creator sign-ups**.
- **Measurement Method**: Full database recalculation, GSC, GA4.
- **Risks & Mitigations**: Handover friction; provide video walkthroughs and automated self-healing scripts.

---

## 7. Master Risk Register & Mitigation Strategy

| Risk ID | Risk Description | Severity | Probability | Impact Area | Proactive Mitigation Strategy |
|:---:|:---|:---:|:---:|:---:|:---|
| **RSK-01** | Google SERP Scraping IP Blocks / CAPTCHAs | High | Med | Data Collection | Use official Serper.dev API with residential proxy rotation; fallback to manual CSV import adapter. |
| **RSK-02** | Google Indexing Delay on New Domain Pages | High | High | Content Reach | Request immediate URL indexing via GSC API; syndicate direct links across active Reddit & YouTube communities. |
| **RSK-03** | AI Models Hallucinating Legacy Competitor Brands | Med | High | AI Visibility | Deploy Schema.org SoftwareApplication JSON-LD and authoritative `llms.txt`; seed data into Wikipedia and Zapier. |
| **RSK-04** | Competitor Retaliation / Accelerated Content Output | Med | Med | Organic Ranking | Focus on hyper-specific workflow questions (silence removal, multi-platform publishing) rather than generic keywords. |
| **RSK-05** | Production Code Regression During Fix Deployment | High | Low | Site Availability | All 20 technical fixes pre-validated via automated pytest suite; staging branch review required before production merge. |

---

## 8. Reporting Cadence & Stakeholder Communication

1. **Weekly Automated Digest (Every Monday 09:00 UTC)**:
   - Generated automatically via `python run_engine.py report`.
   - Delivered to growth team Slack channel with headline KPIs, top ranking changes, and failed collection telemetry.
2. **Monthly Strategic Review (Every 30 Days)**:
   - Live walkthrough on the Streamlit Dashboard (`http://localhost:8502`).
   - Review of competitor Share of Voice shifts (OpusClip, Descript, CapCut) and PR outreach conversion rates.
3. **Quarterly Executive Handover (Day 90)**:
   - Comprehensive ROI summary and forward-looking roadmap for the subsequent 9 months.
