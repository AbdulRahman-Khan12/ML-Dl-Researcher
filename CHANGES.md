# What I customized (quick reference)

This project is built on top of [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher)
(MIT licensed) by the LangChain team. Below is exactly what I changed and why,
so I can talk about it honestly and clearly.

### 1. Re-themed the agent for ML / Deep Learning study  → `src/ml_deep_researcher/prompts.py`
Rewrote the query-writer, summariser, and reflection prompts so the agent
behaves like a tutor building revision notes for an ML/DL student, instead of
a generic web researcher.

### 2. Custom "study notes" report format  → `finalize_summary()` in `graph.py`
The final output now has a titled study-notes section, an auto-generated
"follow-up study questions" section, and a clean de-duplicated sources list.

### 3. Tuned reflection cycles  → `configuration.py`
Default number of research loops changed from 3 → 2 (better speed/depth balance
on a local model), still adjustable from the UI or `.env`.

### 4. New Streamlit front-end  → `app.py`
Added a friendly browser UI (topic box, example buttons, depth slider, status
updates, and a download-notes button). The original only ran in LangGraph Studio.

### 5. Search tool tweak  → `web_research()` in `graph.py`
DuckDuckGo results raised from 3 → 4 so ML topics get an extra source.

### 6. Renaming + docs
Renamed the package to `ml_deep_researcher`, rewrote the README in plain
language, and added this file.

---
**Things I want to learn next:** how LangGraph state actually flows between
nodes, how the JSON-mode structured output works, and how to swap the local
model for a hosted one.
