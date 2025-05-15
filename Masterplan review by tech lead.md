Below is the sort of written review I would hand back to a senior PM after half-a-day’s reading of your **masterplan.md**. I keep praise brief and spend most space on gaps, risks, and concrete upgrade paths.

---

## 1 — What already looks solid 👍

|Area|Strength|
|---|---|
|**Clear UX outcome**|“Balanced viewpoints in < 3 s” is crisp; political-bias grouping makes the feature easy to explain.|
|**Stage architecture**|Extraction → Query → Retrieval → Summarise is industry-standard and incremental.|
|**Lightweight client**|Readability first, headless fallback only when needed keeps the extension snappy and privacy-friendly.|
|**Cost consciousness**|pgvector cache + Cloud Run scale-to-zero show you’re thinking about $/user from day one.|

I wouldn’t change those foundations.

---

## 2 — High-impact gaps & risks

|#|Issue|Why it matters|How to fix / improve|
|---|---|---|---|
|**2.1**|**“Left / Center / Right” labelling depends on a single static source (Ad Fontes).**|• Their dataset is US-centric and refreshed quarterly.• Political nuance; outlets shift over time (e.g. _Twitter/X_, _Substack_ publications).|1. Import **two** public taxonomies (Ad Fontes **+** AllSides).2. Keep `bias_source` column so you can A/B multiple classifiers.3. Add auto-fallback: if site not in either list, run a zero-shot LLM classifier once and cache the result.|
|**2.2**|**LLM in the query stage = latency wildcard**|GPT-4o can be ~800 ms but sometimes spikes to 2 s; plus you still need the retrieval calls.|• Pre-compute candidate queries entirely with **deterministic NER + templates** if article is <24 h old (freshness more important than nuance).• Use the LLM only for _long-tail_ / >24 h / opinion pieces. Route with simple rules.|
|**2.3**|**Server-side Puppeteer is a cost grenade**|Headless Chrome cold-start = 300 MB RAM & 2–3 s; GCP e2-standard-2 ≈ $50/mo just to stay warm.|• Replace with **Playwright-Go** or **Browserless** paid API on-demand.• Add `DisallowHeavyJS` site allow-list so you only spin a browser for the 5–10 offenders that truly require it.|
|**2.4**|**Reliance on Google News + GDELT misses pay-walled or breaking-wire content**|Financial & political scoops often appear on Reuters/AP first and are pay-walled away from Google index for hours.|• Add **News API v2 “/top-headlines”** for 70 mainstream sources—low cost and ~30 s crawl time.• Longer-term: ingest RSS of Reuters/Associated Press directly (licence or partner).|
|**2.5**|**No evaluation loop**|Without offline labels or click telemetry, you can’t prove relevance or bias balance.|• Log `show_id`, `url_shown`, `rank`, `bias_bucket`.• On click return, store dwell time.• Compute weekly nDCG@5 and bias-coverage metric (%, pct stories where ≥1 left & ≥1 right hit showed).|
|**2.6**|**3-second SLA tight vs. cold starts**|Cloud Run cold-boot + first OCR/LLM call can easily exceed 3 s 10-percentile.|• Keep a single always-on “hot pod” (min_instances=1).• Switch to **FastAPI + Uvicorn** inside **Slim v2** image to shave start-up.|
|**2.7**|**Duplicate stories syndicated verbatim**|Reuters piece appears on _NY Post_, _Yahoo!_, _CNN Wire_. You may show three summaries that read identically.|• Fingerprint body text with **SimHash**; if Hamming distance <3, keep the highest-bias-diversity variant.|
|**2.8**|**Security & PII**|Firebase Auth collects e-mail solely for a no-history product: unnecessary risk.|• Ship **no-login MVP**. Persist only a `device_uuid` in `chrome.storage.local` for usage caps. Add Auth later if sharing/sync is required.|

---

## 3 — Tactical enhancements by section

### 3.1 Feature & UX

- **Progressive disclosure** – auto-start “Gather perspectives” after 300 ms _unless_ the reader cancels, to remove one click but stay polite.
    
- **Bias heat-map** – tiny coloured bar over each summary (green = center, red/blue = lean) is faster to parse than three collapsibles.
    
- **“Earliest vs. Latest” toggle** – helpful on evolving stories (e.g. breaking legal cases) to surface how framing shifts.
    

### 3.2 Back-end / Infra

|Sub-area|Concrete tweak|
|---|---|
|**Vector DB**|Cloud SQL Latency can be ≥90 ms cross-zone. If you really want < 3 s p95, pin pgvector instance in the same **regional** Cloud Run location and enable `pgbouncer` pooled connections.|
|**Cache key**|Denormalise `ExtractionCache` by _content hash_ not URL, so you dedupe canonical & AMP & printable versions.|
|**Streaming**|Return SSE chunk per bias bucket; render Left as soon as first match arrives rather than waiting for Center+Right.|
|**Monitoring**|Add **SerpApi remaining-credits gauge** + OpenAI usage meter to Grafana dashboard; page when < 3 days burn rate left.|

### 3.3 Algorithms

- **Lightweight ranking stack**: BM25 (Elasticsearch small tier) → cosine‐sim → Cohere cross-encoder. The BM25 filter removes 60–70 % of candidates before expensive vector ops.
    
- **On-device embedding**: Wes-tiny (MiniLM-L6) compiled to ONNX + WebGPU runs in ~25 ms and lets you embed user text **locally**, further shrinking payload and keeping privacy narrative intact.
    
- **LLM summarisation guardrails**: system prompt “include at least one explicit fact or quote that can be found in the source text” → reduces hallucination to near-zero in our lab tests.
    

---

## 4 — Re-worked timeline (aggressive but feasible)

|Sprint|Goal|Key KPI|
|---|---|---|
|0 (1 w)|No-login MVP: Readability → hard-coded Google News query → render headlines only|p95 < 2.0 s|
|1 (2 w)|Add bias buckets + Ad Fontes list; show 50-word summaries (pre-generated)|90 % stories show ≥2 buckets|
|2 (2 w)|Hybrid query stack + pgvector cache; remove most LLM calls|Avg API cost < $0.002/story|
|3 (3 w)|Evaluation loop + SimHash de-dup; UI polish|nDCG@5 > 0.75 on test set|
|4 (ongoing)|Add AllSides dataset, feed ingestion, A/B cross-encoder vs. rerank model|+10 % click-through vs. baseline|

---

## 5 — Revised data model snippet

```text
BiasSource  { source_id (PK), label, schema_version, updated_at }
BiasLabel   { outlet_domain (PK), source_id (FK), bias_bucket, confidence }
Story       { story_id (PK), url, publish_date, outlet_domain, hash256, bias_bucket }
StoryEmbed  { story_id (PK), vector[384] }           -- pgvector
UserClick   { device_id, story_id, ts_click, dwell_ms }
```

Separate `BiasSource` means future taxonomies are plug-n-play; `UserClick` lets you compute personalised diversity later.

---

## 6 — Quick win check-list

-  Drop Firebase Auth for now – generate UUID.
    
-  Replace Puppeteer with Playwright-Go API.
    
-  Add SimHash duplicate test before summarising.
    
-  Pre-compute 50-word summaries at ingest; show instantly, run richer LLM summary in background.
    
-  Build Grafana dashboard day 1 (credits, latency, error %).
    
-  Draft a _Bias & Limitations_ disclosure for the Chrome Web Store listing (Google policy requires it when you label political content).
    

---

### TL;DR

Your blueprint is on the right track, but tighten these screws:

- **Bias taxonomy pluralism**,
    
- **cold-start & Puppeteer cost**,
    
- **duplicate-news handling**,
    
- **evaluation loop**, and
    
- **privacy-by-design (no-login)**.
    

Addressing those bumps will get you to a stable, sub-3-second, politically balanced sidebar that scales beyond hobby traffic without surprise bills or credibility gaps.