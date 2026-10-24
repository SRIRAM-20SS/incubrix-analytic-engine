# IncuBrix Research Methodology & Question Provenance Framework

## 1. Executive Summary & Objective

Phase 1 of the IncuBrix 2027 Growth Engineer assessment (Option 3: AEO, SEO, and GEO Visibility Engine) establishes a rigorously verified empirical baseline of 100 creator questions across 10 core operational categories. The objective is to understand creator pain points in AI-assisted video workflows, assess IncuBrix's current digital footprint, and identify measurable organic and AI visibility opportunities.

This document details the data provenance protocols, source categorization, deduplication algorithms, and manual-import workflows governing the research pipeline.

---

## 2. Source Classification & Provenance Taxonomy

To prevent data hallucination and ensure audit reproducibility, all research inquiries are categorized into four distinct methodological tiers:

```
[Tier 1: Observable Public Query]  ──> Counted as Real Question (Verified)
[Tier 2: Aggregated Search Demand] ──> Counted as Real Question (Verified)
[Tier 3: Product Inferred Query]   ──> Tracked as Feature Hypothesis (Excluded from Baseline)
[Tier 4: Synthetic / AI Generated] ──> Isolated in Scratch / Brainstorm (Excluded from Baseline)
```

### Tier 1: Real Public Sources (Direct Observation)
- **Source Types**: Google Autocomplete, Google People Also Ask (PAA), Reddit creator forums (`r/podcasting`, `r/ContentCreators`, `r/VideoEditing`, `r/socialmedia`, `r/NewTubers`), YouTube Search Suggestions, and Platform Creator Portals (TikTok Creator Portal).
- **Access Protocol**: Public HTTPS GET requests and incognito search queries. No login bypass, private scraping, or credential violations.
- **What It Legitimately Proves**: Proves active consumer query intent, real-time typing habits, and peer-to-peer technical bottlenecks.
- **Acceptance Rule**: Counted as a verified question when accompanied by a traceable URL and a concrete search/thread evidence snippet.

### Tier 2: Keyword Aggregators & Suggestion Tools
- **Source Types**: AnswerThePublic, Google Suggest API clusters.
- **Access Protocol**: Public search query visualizations and search suggestion trees.
- **What It Legitimately Proves**: Proves historical prepositional search frequency (e.g., questions prefixed with "how to", "can ai", "best tool for", "vs").
- **Acceptance Rule**: Counted as a verified question when cross-referenced against active search engine suggestions.

### Tier 3: Inferred Product Queries (Excluded from Baseline)
- **Definition**: Queries derived logically from internal product capabilities (e.g. "Does IncuBrix support IndexedDB local caching?").
- **Classification**: Treated as product development hypotheses. **Never counted toward the 100-question baseline** unless an equivalent query is independently discovered in Tier 1 or Tier 2 sources.

### Tier 4: Synthetic AI Brainstorming Questions (Excluded from Baseline)
- **Definition**: Queries brainstormed or generated via LLM prompt completions.
- **Classification**: Strictly segregated in experimental directories. **Prohibited from the verified baseline** to maintain absolute research integrity.

---

## 3. The 10 Core Research Categories

The 100 questions are evenly distributed across the creator journey (10 questions per category, minimum 8 required):

1. **AI Content Creation**: Scriptwriting, voiceover synthesis, talking avatars, b-roll generation, thumbnail packaging.
2. **Editing and Enhancement**: Audio denoising, filler word removal, loudness normalization, 4K upscaling, silence trimming, background isolation.
3. **Repurposing Content**: Long-to-short clipping, podcast reels, 9:16 vertical reframing, webinar hooks, batch shorts generation.
4. **Captions and Descriptions**: Hormozi animated subtitle styling, auto emojis, SEO descriptions with timestamps, multi-language translation, hardcoded burning.
5. **Publishing and Scheduling**: Multi-platform syndication (TikTok + Reels + Shorts), direct-from-editor scheduling, custom thumbnail covers, API rate limits.
6. **Content Growth and Engagement**: Retention drop-off analytics, 3-second hook optimization, CTR prediction, viral swipe-away benchmarks, loop mechanics.
7. **AI Tool Comparisons**: Direct 1v1 comparisons (Descript vs OpusClip, Veed vs Kapwing) and multi-tool evaluations.
8. **Pricing and Alternatives**: Free tools without watermarks, freemium tier limitations, credit vs subscription models, open-source alternatives.
9. **Creator Workflows and Productivity**: Solo creator SOPs, b-roll organization, weekly upload velocity, client approval workflows, cloud storage integrations.
10. **Troubleshooting and Best Practices**: Audio-visual desync, upload compression, facial cropping glitches, copyright audio claims, custom jargon pronunciation.

---

## 4. Deduplication & Semantic Normalization Engine

To guarantee that all 100 questions are distinct while preserving original wording and provenance:

1. **String Normalization**:
   - Strips leading/trailing interrogative symbols (`?`, `!`, `.`, `:`, quotes).
   - Replaces non-alphanumeric punctuation with whitespace.
   - Collapses contiguous whitespace into single spaces and lowercases all characters.
2. **Exact Duplicate Detection**:
   - Maps normalized strings to unique Question IDs (`Q001` - `Q100`).
   - Flags identical semantic duplicates immediately.
3. **Near-Duplicate / Semantic Similarity Detection**:
   - Implements Jaccard token similarity with lightweight plural/suffix stemming:
     $$\text{Jaccard}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
   - Flags pairs with similarity scores $\ge 0.85$ for human editorial review to eliminate redundant question variants.

---

## 5. Validation Rules & Automated Quality Gates

The automated validator (`src/research/validate_questions.py`) executes 6 rigorous validation layers:

| Validation Layer | Criterion | Action on Failure |
| :--- | :--- | :--- |
| **Mandatory Schema** | All 15 required columns present and non-empty | Row marked `Rejected` |
| **URL Syntax** | Valid HTTP/HTTPS protocol with resolvable netloc | Row marked `Rejected` |
| **Date Standard** | Valid ISO 8601 format (`YYYY-MM-DD`) | Row marked `Rejected` |
| **Category Standard** | Exactly matches one of the 10 approved categories | Row marked `Rejected` |
| **Evidence Standard** | `source_evidence` must be $\ge 10$ chars and not identical to `source_url` | Row marked `Pending` |
| **Category Sufficiency**| Each of the 10 categories must have $\ge 8$ verified questions | Pipeline flags deficiency |

---

## 6. Manual-Import & Fallback Workflow

When automated crawlers or autocomplete endpoints encounter rate limiting (HTTP 429) or geographic restrictions:

1. **Do Not Bypass Security**: The pipeline strictly complies with site terms and never uses unauthorized scraping proxies.
2. **Documented Manual Import**:
   - Sourced entries are recorded into `data/research/manual_import_template.csv`.
   - The researcher populates the 15 required fields directly from manual browser verification.
   - The pipeline ingests the manual CSV via `load_questions_from_csv("path/to/file.csv")`.
   - Full automated validation and deduplication are executed on the imported dataset.
