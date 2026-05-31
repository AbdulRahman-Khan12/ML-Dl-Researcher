"""
ML & Deep Learning Study Research Agent — Streamlit front-end
=============================================================

MY CUSTOMIZATION:
The original project only ran inside "LangGraph Studio" (a developer tool).
I added this small Streamlit web app so the agent has a simple, friendly
interface that anybody can use: type an ML/DL topic, pick how deep it should
research, click a button, and read the generated study notes in the browser.

How it works (high level):
  1. We import the compiled LangGraph `graph` from the package.
  2. We collect the user's topic + settings from the Streamlit sidebar.
  3. We call graph.invoke(...) which runs the whole agent loop:
        generate query -> web search -> summarise -> reflect -> (repeat) -> finalise
  4. We display the final study-note report.

Run it with:
    streamlit run app.py
"""

import streamlit as st
from langchain_core.runnables import RunnableConfig

# Import the compiled agent graph and the config helper from our package.
from ml_deep_researcher.graph import graph

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ML & DL Study Research Agent",
    page_icon="📚",
    layout="centered",
)

# ---------------------------------------------------------------------------
# A little CSS to make the default Streamlit look softer and tidier.
# (Just spacing, rounded corners and nicer buttons — nothing fancy.)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
      /* give the page a bit more breathing room */
      .block-container { padding-top: 2.5rem; max-width: 780px; }

      /* headings */
      h1 { font-weight: 700; letter-spacing: -0.5px; }

      /* make every button rounded and full-width with a smooth hover */
      .stButton > button {
          border-radius: 10px;
          border: 1px solid #e2dfd8;
          padding: 0.5rem 1rem;
          font-weight: 500;
          transition: all 0.15s ease-in-out;
      }
      .stButton > button:hover {
          border-color: #3b6ea5;
          color: #3b6ea5;
      }

      /* text input rounded corners */
      .stTextInput > div > div > input {
          border-radius: 10px;
      }

      /* subtle divider spacing */
      hr { margin: 1.5rem 0; opacity: 0.4; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📚 ML & Deep Learning Study Research Agent")
st.caption(
    "Give it any Machine Learning or Deep Learning topic. It searches the web, "
    "summarises what it finds, reflects on what's still missing, searches again, "
    "and hands you clean study notes with sources."
)

st.write("")  # small gap

# ---------------------------------------------------------------------------
# Sidebar: the knobs the user can turn
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    model_name = st.text_input(
        "Ollama model name",
        value="mistral",
        help="The local model you pulled with Ollama, e.g. 'mistral' or 'llama3.2'. "
        "Run `ollama list` to see what you have. "
        "Make sure Ollama is running before you search.",
    )

    research_depth = st.slider(
        "Research depth (reflection cycles)",
        min_value=1,
        max_value=4,
        value=2,
        help="How many times the agent searches, summarises and reflects. "
        "More cycles = richer notes but slower.",
    )

    st.markdown("---")
    st.info(
        "**Tip:** Start with depth 1 to check everything works, "
        "then increase it once you're happy.",
        icon="💡",
    )
    st.markdown(
        "<small>Made by **idontliketo** · built on LangGraph + Ollama · "
        "search powered by free DuckDuckGo.</small>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main area: the input box + run button
# ---------------------------------------------------------------------------
# Keep the chosen topic in session_state so the example buttons can fill it in.
if "topic" not in st.session_state:
    st.session_state.topic = ""

# Some example topics so a beginner isn't staring at a blank box.
st.markdown("**Need ideas? Tap one to get started:**")
examples = [
    "Transformer self-attention",
    "Overfitting vs underfitting",
    "Convolutional neural networks",
    "Gradient descent optimizers",
]
cols = st.columns(len(examples))
for i, example in enumerate(examples):
    if cols[i].button(example, use_container_width=True):
        st.session_state.topic = example

topic = st.text_input(
    "🔍 What ML/DL topic do you want to study?",
    key="topic",
    placeholder="e.g. How does backpropagation work in neural networks?",
)

st.write("")  # small gap
run = st.button("🚀 Research this topic", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Run the agent
# ---------------------------------------------------------------------------
if run:
    if not topic.strip():
        st.warning("Please type a topic first 🙂")
    else:
        # Build the configuration that the graph expects. These values flow
        # into our Configuration class (configuration.py).
        config = RunnableConfig(
            configurable={
                "local_llm": model_name,
                "llm_provider": "ollama",
                "search_api": "duckduckgo",
                "max_web_research_loops": research_depth,
            }
        )

        with st.status("Researching… this can take a minute on a local model.", expanded=True) as status:
            try:
                st.write(f"📝 Topic: **{topic}**")
                st.write(f"🔁 Running {research_depth} research cycle(s)…")

                # This single call runs the WHOLE agent loop and returns the
                # final state. The output schema gives us 'running_summary'.
                result = graph.invoke({"research_topic": topic}, config=config)

                status.update(label="✅ Done! Study notes are ready.", state="complete")
            except Exception as e:
                status.update(label="❌ Something went wrong.", state="error")
                msg = str(e).lower()

                # Show advice that matches the actual failure instead of always
                # blaming Ollama, which is confusing when search is the problem.
                if "duckduckgo" in msg or "search failed" in msg or "rate-limit" in msg:
                    st.error(
                        "The **web search** step failed — this is almost always "
                        "DuckDuckGo temporarily rate-limiting free requests.\n\n"
                        "**What to do:** wait a few seconds and click "
                        "**Research** again. It usually works on the next try.\n\n"
                        f"Technical detail: `{e}`"
                    )
                else:
                    st.error(
                        "The agent could not finish. The most common reasons are:\n\n"
                        "1. **Ollama isn't running** — open the Ollama app / run `ollama serve`.\n"
                        "2. **The model isn't downloaded** — run `ollama pull mistral`.\n"
                        "3. **No internet** — DuckDuckGo search needs a connection.\n\n"
                        f"Technical detail: `{e}`"
                    )
                result = None

        if result and result.get("running_summary"):
            st.markdown("---")
            st.subheader("📝 Your study notes")

            # Show the notes inside a bordered card. Using Streamlit's own
            # container (instead of a raw HTML div) means the markdown inside
            # — headings, links, bullet points — still renders properly.
            with st.container(border=True):
                st.markdown(result["running_summary"])

            st.write("")  # small gap

            # Let the student download the notes as a markdown file.
            st.download_button(
                "💾 Download these notes (.md)",
                data=result["running_summary"],
                file_name=f"study_notes_{topic[:30].replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
