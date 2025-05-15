Below is a tech-lead–style blueprint that turns your **Political Perspectives Sidebar** vision into a clean, modular project you can scale and maintain. It’s organized so that each phase delivers a meaningful slice of end-to-end value while keeping the blast radius small if you need to pivot. &#x20;

---

## 1. High-Level Development Workflow

| Phase                                | Goal                                       | Primary Deliverables                                                                         | “Definition of Done”                              |
| ------------------------------------ | ------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **0 — Bootstrap**                    | Repo, CI/CD, basic lint/test scaffolding   | Git monorepo, GitHub Actions, Conventional Commits                                           | PR merges run tests & lints automatically         |
| **1 — MVP Content Extraction**       | Reliable article text in the browser       | Chrome extension skeleton, `contentScript`, Readability-based extractor, sidebar placeholder | Click icon → sidebar shows extracted text in <3 s |
| **2 — Backend Retrieval Pipeline**   | From article text to candidate URLs        | Containerized Cloud Run service with REST endpoints: `/topics`, `/search`, `/dedupe`         | Local curl test returns unique article list       |
| **3 — Summarization & Bias Tagging** | Produce 120-word summaries + bias metadata | Summarizer & bias annotator microservice; Postgres + pgvector cache                          | Endpoint returns JSON: `{left, center, right}`    |
| **4 — Full Stack Integration**       | Wire sidebar to backend                    | Sidebar React components, loading states, error handling                                     | End-to-end flow completes for 1 live article      |
| **5 — User Layer**                   | Auth & preferences                         | Firebase Auth, settings panel, basic Firestore doc                                           | User login persists settings locally & remotely   |
| **6 — Hardening & Observability**    | Scale & monitor                            | Cloud Logging dashboards, SLO alerts, e2e test suite                                         | <1 % error rate in staging load test              |

---

## 2. Repository & File Structure (Monorepo)

```
political-perspectives/
├── .github/
│   └── workflows/        # CI pipelines
├── extension/
│   ├── manifest.json
│   ├── src/
│   │   ├── contentScript.ts
│   │   ├── sidebar/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── components/
│   │   │   └── hooks/
│   │   ├── utils/
│   │   └── styles/
│   ├── public/           # icons, HTML entrypoints
│   └── tests/
├── backend/
│   ├── shared/           # dataclasses, exceptions, logging cfg
│   │   ├── models.py
│   │   └── config.py
│   ├── services/
│   │   ├── extraction/
│   │   │   ├── main.py   # FastAPI router
│   │   │   └── article_extractor.py
│   │   ├── topics/       # spaCy + BERTopic
│   │   ├── query_gen/    # Gemma 3 prompt wrapper
│   │   ├── retrieval/    # GDELT / SERPAPI fan-out
│   │   ├── dedup/        # SimHash + MMR pgvector
│   │   ├── summarizer/   # map-reduce LLM calls
│   │   └── bias/         # Ad Fontes lookup
│   ├── infra/
│   │   ├── Dockerfile
│   │   └── cloudrun.yaml
│   └── tests/
├── infra/                # IaC outside Cloud Run
│   ├── terraform/
│   └── monitoring/
└── scripts/              # one-off admin & seed scripts
```

---

## 3. Backend Module Breakdown

| Layer                  | Key Class / Function                    | Responsibility                       |                                                   |
| ---------------------- | --------------------------------------- | ------------------------------------ | ------------------------------------------------- |
| **Extraction**         | \`ArticleExtractor.extract(url          | html)\`                              | Clean body & title with Trafilatura / Readability |
| **Topic Detection**    | `TopicDetector.get_topics(text)`        | Named entities + BERTopic clusters   |                                                   |
| **Query Generation**   | `QueryGenerator.build_queries(topics)`  | LLM function-call → list\[str]       |                                                   |
| **Retrieval**          | `SearchAggregator.search(queries)`      | Fan-out to GDELT, News API, SERPAPI  |                                                   |
| **Deduplication**      | `Deduplicator.group_by_simhash(docs)`   | Near-duplicate clustering            |                                                   |
| **Semantic Filtering** | `MMRSelector.select(diverse_docs, k)`   | pgvector-powered diversity rank      |                                                   |
| **Summarization**      | `Summarizer.summarize(doc)`             | 120-word map-reduce summary          |                                                   |
| **Bias Annotator**     | `BiasLabeler.lookup(source)`            | Returns `{'bias':'Left', 'score':…}` |                                                   |
| **Formatter**          | `PerspectiveFormatter.to_payload(docs)` | Package JSON for sidebar             |                                                   |
| **Auth / Prefs**       | Firebase; minimal service wrapper       | Verify ID token, fetch prefs         |                                                   |

All services expose FastAPI routers so you can compose them under one Cloud Run container or later split into separate containers on the same interface contract.

---

## 4. Chrome Extension Modules

| Folder                | Purpose                                                          |
| --------------------- | ---------------------------------------------------------------- |
| `contentScript.ts`    | Injected into page; pulls article HTML; posts message to sidebar |
| `sidebar/Sidebar.tsx` | Top-level React component; orchestrates UI states                |
| `components/`         | `PerspectiveCard`, `Loader`, `ErrorToast`, toggle controls       |
| `hooks/`              | `useExtraction()`, `usePerspectives()`, `useAuth()`              |
| `utils/`              | `fetchWithTimeout`, local storage helpers                        |
| `styles/`             | Tailwind config, tokens for bias colors                          |
| `tests/`              | Jest + React Testing Library                                     |

---

## 5. Step-by-Step Implementation Order

1. **Repo & Tooling**

   * Initialize monorepo, Prettier/ESLint, Black/isort, pre-commit hooks.

2. **Chrome Extension Skeleton**

   * `manifest.json`, minimal popup, hot-reload setup.

3. **`contentScript` + Readability POC**

   * Extract plain text; render in raw sidebar; unit test extraction fallback flows.

4. **Backend ― Extraction Microservice**

   * FastAPI scaffold; implement `ArticleExtractor`; containerize; deploy to dev Cloud Run.

5. **Topic Detection & Query Generation**

   * Integrate spaCy, BERTopic; mock Gemma 3 call; return static queries for unit tests.

6. **Search Aggregator**

   * Write GDELT adapter; stub News API & SERPAPI; build retries/exponential backoff.

7. **Deduplication & Semantic Filtering**

   * Implement SimHash grouping; set up Postgres + pgvector dev instance; MMR selector.

8. **Summarizer & Bias Annotator**

   * Integrate chosen LLM provider; map-reduce wrapper; Ad Fontes CSV seed into Postgres.

9. **Perspective Formatter & API Gateway**

   * One endpoint `/perspectives` stitches the pipeline; returns final payload.

10. **Sidebar React Components**

    * Build `PerspectiveCard`, loaders, collapse sections; consume `/perspectives`.

11. **User Auth & Preferences**

    * Firebase Web SDK; store “bias default open” preference in Firestore.

12. **Caching Layers**

    * Redis HTML cache in front of extraction; query result TTL; Cloud Memorystore setup.

13. **Observability & Alerts**

    * Structured logging; Google Cloud Error Reporting; uptime checks.

14. **Automated Tests & Load Testing**

    * Write e2e Cypress tests; Locust or k6 load tests for `/perspectives`.

15. **Security & Privacy Review**

    * Chrome Web Store checklist; CSP headers; GDPR data flow diagram.

16. **Beta Launch & Feedback Loop**

    * Release to ≤100 users; log performance; iterate on latency hot spots.

---

Below is a **contract-level specification** for the Political Perspectives platform.
It turns the earlier module breakdown into concrete REST/Message contracts so every team (extension, backend, DevOps, QA) can work independently yet stay interoperable. &#x20;

---

## 0. Conventions

| Area        | Standard                                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| Transport   | HTTPS + JSON over REST                                                                                              |
| Auth        | `Authorization: Bearer <Firebase ID token>` (Chrome extension passes the token it already holds)                    |
| Timeouts    | Client ⇒ API: 7 s (default); Internal service-to-service: 3 s                                                       |
| Idempotency | All POSTs that change state accept optional `Idempotency-Key` header                                                |
| Error model | Non-200 responses return `{code, message, details?}` with gRPC-style codes (`NOT_FOUND`, `DEADLINE_EXCEEDED`, etc.) |
| Dates       | RFC 3339 strings in UTC (`2025-05-15T09:34:12Z`)                                                                    |

---

## 1. API-Gateway Surface (single public base URL)

This “edge” FastAPI app simply **orchestrates** calls to the deeper micro-services and applies auth / rate-limit / caching. All endpoints are versioned (`/v1/…`).

| Method | Path               | Purpose                                                                              | Typical Latency |
| ------ | ------------------ | ------------------------------------------------------------------------------------ | --------------- |
| `POST` | `/v1/extract`      | Clean article text from a given URL or raw HTML                                      | 400 ms          |
| `POST` | `/v1/topics`       | Named-entity + BERTopic clusters                                                     | 250 ms          |
| `POST` | `/v1/queries`      | LLM-driven query generation                                                          | 600 ms          |
| `POST` | `/v1/search`       | Multi-source fan-out & HTML extraction                                               | 1.1 s           |
| `POST` | `/v1/dedup`        | SimHash grouping + canonical pick                                                    | 120 ms          |
| `POST` | `/v1/filter`       | pgvector MMR selection                                                               | 150 ms          |
| `POST` | `/v1/summarize`    | 120-word LLM map-reduce summary                                                      | 850 ms          |
| `POST` | `/v1/bias`         | Ad Fontes lookup for a source                                                        | 20 ms           |
| `POST` | `/v1/perspectives` | **Composite pipeline** that runs ➊-➑ above and returns final payload for the sidebar | ≤ 3 s           |

> 🔹 Staged rollout: start with only `/perspectives` exposed → open individual endpoints later for tooling & A/B tests.

---

### 1.1  `/v1/perspectives`  (happy-path payload)

```jsonc
POST /v1/perspectives
{
  "url": "https://www.nytimes.com/2025/05/15/politics/senate-budget.html",
  "html": null  // optional raw HTML if user triggered extraction manually
}

200 OK
{
  "source": {
    "title": "Senate Passes …",
    "publish_date": "2025-05-15",
    "bias": "Center",
    "summary": "…120-word extract…"
  },
  "alternatives": {
    "Left": [
      {
        "title": "Budget Sparks Backlash …",
        "url": "https://slate.com/article.html",
        "summary": "…",
        "publish_date": "2025-05-15",
        "bias_score": -6
      }
    ],
    "Center": [ … ],
    "Right": [ … ]
  },
  "meta": {
    "processing_ms": 2840,
    "llm_tokens": 1956,
    "cache_hit": false
  }
}
```

| Status | Meaning                                                    |
| ------ | ---------------------------------------------------------- |
| `200`  | Success                                                    |
| `429`  | User over daily quota (70 analyses × day per master plan)  |
| `400`  | Invalid URL / HTML                                         |
| `500`  | Upstream timeout (details include failing stage)           |

---

## 2. Micro-service Contracts

Below each service exposes a **FastAPI router** registered under its name; internal calls use the same JSON shapes but skip Firebase validation.

### 2.1 Article Extractor `/extract`

| Field   | Type      | Notes                                   |
| ------- | --------- | --------------------------------------- |
| `url`   | *string*  | Mutually exclusive with `html`          |
| `html`  | *string?* | Raw HTML when provided by the extension |
| `force` | *bool?*   | `true` → bypass Redis/page cache        |

**Response**

```json
{
  "clean_text": "<5-10k chars>",
  "title": "Original headline",
  "language": "en",
  "chars": 9321
}
```

Errors: `INVALID_ARGUMENT` (both url & html), `UNREADABLE` (JS-rendered page needs Puppeteer later).

---

### 2.2 Topic Detector `/topics`

```json
POST /topics
{
  "text": "<clean_text>",
  "max_topics": 8
}
```

```json
{
  "entities": ["US Senate", "budget", "Medicare"],
  "topics": ["Fiscal policy", "Healthcare funding"],
  "confidence": 0.87
}
```

---

### 2.3 Query Generator `/queries`

```json
POST /queries
{
  "topics": ["Fiscal policy", "Healthcare funding"],
  "entities": ["US Senate"]
}
```

```json
{
  "queries": [
    "site:news \"US Senate\" Medicare budget negotiations",
    "\"Fiscal policy\" AND Senate budget 2025"
  ],
  "model": "gemma-3b-it",
  "tokens": 96
}
```

---

### 2.4 Search Aggregator `/search`

```json
POST /search
{
  "queries": [ … ],
  "sources": ["GDELT", "NEWS_API", "SERPAPI"],
  "max_per_query": 20
}
```

Response returns **deduplicated URL list** plus lightweight metadata ready for deep extraction.

---

### 2.5 Deduplicator `/dedup`

Input: list of `{url, title, hash}` →
Output: list of **representative** docs, each with `duplicate_of` array.

---

### 2.6 Semantic Filter `/filter`

```json
POST /filter
{
  "docs": [{ "url": "...", "embedding": [0.03, …] }],
  "seed_url": "https://nytimes.com/…",
  "k": 9,
  "lambda": 0.7   // MMR trade-off
}
```

Returns top-k diverse docs ordered for presentation.

---

### 2.7 Summarizer `/summarize`

```json
POST /summarize
{
  "url": "https://www.foxnews.com/…",
  "text": "<clean_text>",
  "max_tokens": 300
}
```

Response adds `summary`, `llm_model`, `tokens_used`, `avg_chunk_ppl`.

---

### 2.8 Bias Annotator `/bias`

Input `{ "source": "Fox News" }` → returns `{ "bias": "Right", "bias_score": 15 }`.

---

## 3. Chrome Extension ⇄ Backend Contract

| Channel                                                 | Payload shape                                             | When                          |
| ------------------------------------------------------- | --------------------------------------------------------- | ----------------------------- |
| **`window.postMessage`** from `contentScript` → sidebar | `{type:"PP_FETCH", url, html?}`                           | On icon click                 |
| Sidebar React hook calls **`/v1/perspectives`**         | `{url, html?}`                                            | Immediately after extraction  |
| **`chrome.storage.sync`**                               | `{userPrefs}`                                             | Toggle bias groups, font size |
| **Firebase Auth**                                       | Handled in background script; ID token cached & refreshed | Every 55 min                  |

---

## 4. Sequence Diagram (textual)

```
contentScript → sidebar: postMessage(url)
sidebar → API /perspectives: POST
/perspectives → extractor
extractor → topicDetector
topicDetector → queryGenerator
queryGenerator → searchAggregator
searchAggregator → deduplicator → semanticFilter
semanticFilter → summarizer
summarizer → biasAnnotator
biasAnnotator → /perspectives
/perspectives → sidebar: JSON payload
sidebar → React UI: render cards
```

All hops except extractor/search run inside the same Cloud Run container initially, keeping network latencies low.

---

## 5. Non-Functional Guarantees

| Metric                          | Target | Alert at         |
| ------------------------------- | ------ | ---------------- |
| **P99 `/perspectives` latency** | ≤ 3 s  | >3.5 s 5-min avg |
| **Error rate**                  | < 1 %  | ≥ 2 %            |
| **LLM token spend/user/day**    | ≤ 15 k | > 18 k           |

Monitoring wired via Cloud Logging & Error Reporting as specified in the master plan.&#x20;

---

### Next Action → Implementation

1. **Define Pydantic request/response models** mirroring the above shapes.
2. Stub each router with `TODO` to call its successor, enabling incremental dev.
3. Set up **contract tests (pytest + Schemathesis)** so future schema tweaks fail CI.

When you give the green light, we can start writing those Pydantic models and FastAPI stubs.
