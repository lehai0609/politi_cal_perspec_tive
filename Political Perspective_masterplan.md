## 1. App Overview & Objective
**Name (TBD):** Political Perspectives Sidebar  
**Objective:**  
Enable readers to gain balanced insights by surfacing concise summaries of how left-, center-, and right-leaning outlets cover the same news story—directly in a Chrome sidebar, in under 3 seconds per request, while keeping costs controlled and preserving precision.

---

## 2. Target Audience
- **Primary:** Politically engaged news readers seeking balanced viewpoints  
- **Secondary:** Educators, researchers, and civically minded users looking for media-bias context  
- **Usage Pattern:**  
  - ≤100 early adopters  
  - Up to 70 article analyses per user per day  
  - English-language articles only (MVP)

---

## 3. Core Features & Functionality
1. **In-page Extraction**  
   - Use Mozilla Readability  in the client to grab clean text  
   - (Final fallback: User guide extraction) Ask user for copy and paste content of article into extension's sidebar.

2. **Topic Detection & Query Formulation**  
   - spaCy NER + BERTopic clustering for entities & themes  
   - LLM function-call to generate structured search queries.  Specifically utilize Gemma 3 for quick & cheap implementation of query formulation.
   - Cohere ReRank (or similar) to pick the top 5 search hints  

3. **Multi-Source Retrieval & Filtering**  
	-  **Fan-out Queries:** Send your top queries (from Stage 2) to GDELT, News API, and SERPAPI (as a fallback or additional source).
	- **Initial Retrieval:** Gather all results.
	- **Extraction & Cleaning:** For each retrieved article URL, extract the main content (using your Stage 1 logic).
	- **Textual Deduplication:**
	    - Calculate SimHash (or a strong content hash) of the extracted body text for each article.
	    - Group identical/near-identical articles.
	    - From each group of duplicates, select the representative article based on source bias diversity or other heuristics (e.g., preferring the original source if identifiable, or the one from the most reputable source in the cluster).
	- **Semantic Filtering/Ranking for Diversity (using pgvector):**
	    - For the unique articles remaining after textual deduplication:
	        - Generate embeddings for their headlines/snippets (or full text if feasible and beneficial for MMR).
	        - Use these embeddings with your pgvector cache. You could:
	            - Filter out articles that are too semantically similar to already selected high-quality articles from different perspectives.
	            - Or, more powerfully, use MMR to select a diverse set of N articles that are relevant to the input topics/entities.
	- **Prepare for Summarization:** The output of this stage is a clean, de-duplicated, and potentially diversity-ranked list of articles ready for Stage 4 (Summarization & Presentation).
4. **Summarization & Presentation**  
   - Map-reduce LLM summarization, capped at ~120 words per source  
   - Include publish date & bias rating (Ad Fontes database)  
   - Sidebar UI:  
     - Click extension → confirm story → “Gather Perspectives”  
     - Expand/collapse sections for Left / Center / Right  
     - “No alternatives found” message when empty  

5. **User Auth & Preferences**  
   - Firebase Auth (email/password + Google/Twitter OAuth)  
   - Store only basic profile in Firestore (no history)

---

## 4. High-Level Technical Stack
| Layer                    | Service / Library                      | Why                                                         |
| ------------------------ | -------------------------------------- | ----------------------------------------------------------- |
| **Client**               | Chrome Extension + Mozilla Readability | Instant, privacy-safe extraction; minimal bundle size       |
| **Backend Compute**      | Google Cloud Run                       | Containerized Python NLP + LLM orchestration; scale-to-zero |
| **NLP & Extraction**     | Trafilatura, spaCy, BERTopic, Gemma 3  | Balanced precision, cost & performance                      |
| **Search APIs**          | SERPAPI (Google News), GDELT DOC 2.0   | Coverage, multi-lingual fallback                            |
| **Vector Cache**         | Cloud SQL (Postgres) + pgvector        | Efficient semantic filtering & MMR                          |
| **HTML Cache**           | Cloud Memorystore (Redis)              | Low-latency caching of rendered pages                       |
| **User Data**            | Firestore                              | Serverless profiles store                                   |
| **Auth**                 | Firebase Auth                          | Turnkey email/OAuth                                         |
| **Monitoring & Logging** | Cloud Logging & Error Reporting        | Track errors, performance metrics                           |

---

## 5. Conceptual Data Model
```text
User {
  user_id (PK)
  email
  oauth_providers [google, twitter]
}

BiasRating {
  source_name (PK)
  bias_score  // from Ad Fontes database
}

ExtractionCache {
  url (PK)
  cleaned_text
  rendered_html
  timestamp
}

QueryCache {
  query_text (PK)
  candidate_urls [url1, url2, …]
  timestamp
}

Summary {
  url (PK)
  bias_score
  publish_date
  summary_text
}
```

## 6. UI/UX Principles

- **Speed & Clarity:** Show “loading” and then fully rendered sidebar within 3 seconds
- **Hierarchy & Scanning:**
    - Clear headings: Left | Center | Right
    - Collapse/expand toggles for each source group
- **Feedback & Recovery:**
    - “No alternatives found” state
    - Retry button if extraction or retrieval errors occur
- **Theming:**
    - Modern, minimal styling (e.g. Tailwind or Chrome UI guidelines)
    - Subtle color accents to signal political lean (red vs. blue vs. neutral gray)