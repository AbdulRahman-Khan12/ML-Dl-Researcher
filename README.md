# 📚 ML & Deep Learning Study Research Agent

Hey! 👋 This is a small AI **agent** I built to help study Machine Learning and Deep Learning topics.

You give it a topic — like *"How does backpropagation work?"* — and instead of giving one answer and stopping, it works more like a curious student digging into the subject:

1. It writes a focused web search query.
2. It searches the web (free, using DuckDuckGo).
3. It reads through what it found and condenses it into study notes.
4. It **reflects** on those notes and asks *"what am I still missing?"*
5. It searches again to fill that gap.
6. After a couple of these cycles, it puts together clean **study notes with sources**.

That "search → summarise → reflect → search again" loop is what makes it an *agent* rather than a regular chatbot — it decides its own next step based on what it has learned so far.

---

## 🎬 What it looks like

You type a topic in the box, choose how deep you want it to go, and it produces formatted study notes you can download.

> _(Tip: record a short screen GIF of the app running and drop it here — a visible demo goes a long way.)_

---

## 🙌 Honest credit (please read)

I did **not** invent the core research loop. This project is built on top of the excellent open-source [**local-deep-researcher**](https://github.com/langchain-ai/local-deep-researcher) by the LangChain team (MIT licensed).

Here's what **I** changed to turn it into an ML/DL study tool:

| # | What I changed | Where |
|---|----------------|-------|
| 1 | **Re-themed the whole agent as an ML/Deep-Learning study assistant.** I rewrote every prompt (query writer, summariser, reflection) so the model thinks like a tutor making revision notes for a student, not a generic researcher. | `src/ml_deep_researcher/prompts.py` |
| 2 | **Changed the report format to "study notes".** The final output now has a titled notes section, an auto-generated *"follow-up study questions"* section, and a clean sources list — instead of a plain summary. | `finalize_summary()` in `src/ml_deep_researcher/graph.py` |
| 3 | **Tuned the reflection cycles.** Changed the default number of research loops from 3 → 2 (a good balance of depth vs. speed on a local model) and made it adjustable. | `src/ml_deep_researcher/configuration.py` |
| 4 | **Built a Streamlit web front-end.** The original only ran inside a developer tool (LangGraph Studio). I added a browser UI with example topics, a depth slider, and a "download notes" button. | `app.py` |
| 5 | **Tweaked the search tool.** Bumped DuckDuckGo results from 3 → 4 so ML topics get one extra source for both intuition and implementation. | `web_research()` in `src/ml_deep_researcher/graph.py` |
| 6 | **Rewrote this README** in plain language and renamed the package to `ml_deep_researcher`. | this file + `pyproject.toml` |

I'm still learning the deeper parts of LangGraph, and I've left comments throughout the code marking exactly what I changed and why.

---

## 🧠 How it works (the agent loop)

```
        ┌──────────────┐
        │ generate_query│  ← LLM writes a focused ML/DL search query
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │ web_research │  ← DuckDuckGo finds sources (free, no API key)
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │   summarize  │  ← LLM turns sources into study notes
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │   reflect    │  ← LLM asks "what's still missing?" → new query
        └──────┬───────┘
               ▼
         (loop N times)
               ▼
        ┌──────────────┐
        │  finalize    │  ← formats the final study-note report
        └──────────────┘
```

This is built with **LangGraph**, which lets you describe an agent as a graph of steps (nodes) connected by arrows (edges). The loop back from *reflect* to *web_research* is what makes it iterative.

---

## 🚀 Getting started

### What you need
- **Python 3.10 or newer**
- **[Ollama](https://ollama.com/download)** installed (runs the AI model locally on your own machine — free, no API keys, works offline once the model is downloaded)
- An internet connection (for the web search step)

### Step 1 — Get the code
```bash
git clone https://github.com/YOUR_USERNAME/ml-deep-researcher.git
cd ml-deep-researcher
```

### Step 2 — Create a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
**Mac / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install the project
```bash
pip install -e .
```

### Step 4 — Download a local model with Ollama
Open the Ollama app (or run `ollama serve`), then in a terminal:
```bash
ollama pull llama3.2
```

### Step 5 — Run the app! 🎉
```bash
streamlit run app.py
```
Your browser opens at `http://localhost:8501`. Type a topic, pick a depth, and hit **Research this topic**.

---

## ⚙️ Settings you can change

Adjust these from the sidebar in the app, or via a `.env` file (copy `.env.example` to `.env`):

| Setting | What it does | Default |
|---------|--------------|---------|
| Ollama model | Which local model to use | `llama3.2` |
| Research depth | How many search→reflect cycles to run | `2` |
| Search API | Which search engine to use | `duckduckgo` (free) |

---

## 🛠️ Troubleshooting

- **"Connection refused" / agent fails instantly** → Ollama isn't running. Open the Ollama app or run `ollama serve`.
- **"model not found"** → run `ollama pull llama3.2` first.
- **It's slow** → that's normal for local models. Set research depth to 1 while testing and use a small model like `llama3.2`.
- **Search returns nothing** → check your internet connection; DuckDuckGo occasionally rate-limits, so wait a moment and try again.

---

## 📂 Project structure

```
ml-deep-researcher/
├── app.py                          # Streamlit web UI (my addition)
├── src/ml_deep_researcher/
│   ├── graph.py                    # the agent loop (LangGraph nodes + edges)
│   ├── prompts.py                  # ML/DL study prompts (rewritten by me)
│   ├── configuration.py            # settings + defaults (tuned by me)
│   ├── state.py                    # what data flows through the graph
│   ├── utils.py                    # search helpers (DuckDuckGo, etc.)
│   └── lmstudio.py                 # optional LMStudio support
├── .env.example                    # example settings
├── pyproject.toml                  # dependencies
└── README.md                       # you're reading it
```

---

## 📜 License

MIT — same as the original project this is built on. See `LICENSE`.

## 🙏 Acknowledgements

- [langchain-ai/local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) — the original project I learned from and built on.
- [Ollama](https://ollama.com) — for making local LLMs easy.
- [LangGraph](https://langchain-ai.github.io/langgraph/) — for the agent framework.
