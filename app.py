import time
import streamlit as st

st.set_page_config(
    page_title="Research Swarm",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------------
ACCENT = "#7CFFB2"      # signal green
ACCENT_DIM = "#3A6B52"
BG = "#0B0E11"
PANEL = "#12161B"
PANEL_BORDER = "#222831"
TEXT = "#E8ECEF"
SUBTEXT = "#8A93A0"
DANGER = "#FF6B6B"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(circle at 15% 0%, rgba(124,255,178,0.06), transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(124,255,178,0.04), transparent 35%),
        {BG};
    color: {TEXT};
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.hero {{
    border: 1px solid {PANEL_BORDER};
    background: linear-gradient(180deg, rgba(124,255,178,0.05), rgba(124,255,178,0));
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
}}
.hero-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    color: {ACCENT};
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.hero-title {{
    font-size: 2.1rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    letter-spacing: -0.02em;
}}
.hero-sub {{
    color: {SUBTEXT};
    font-size: 0.95rem;
    max-width: 640px;
}}

.pipeline-wrap {{
    display: flex;
    gap: 0;
    margin: 6px 0 30px 0;
}}
.stage {{
    flex: 1;
    position: relative;
    padding: 16px 18px;
    border: 1px solid {PANEL_BORDER};
    background: {PANEL};
    margin-right: -1px;
}}
.stage:first-child {{ border-radius: 12px 0 0 12px; }}
.stage:last-child {{ border-radius: 0 12px 12px 0; }}
.stage-idx {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: {SUBTEXT};
    letter-spacing: 0.1em;
}}
.stage-name {{
    font-weight: 600;
    font-size: 0.95rem;
    margin-top: 4px;
}}
.stage-role {{
    font-size: 0.76rem;
    color: {SUBTEXT};
    margin-top: 2px;
}}
.stage-pending {{ opacity: 0.55; }}
.stage-active {{
    border-color: {ACCENT};
    box-shadow: 0 0 0 1px {ACCENT}, 0 0 24px rgba(124,255,178,0.15);
}}
.stage-active .stage-idx {{ color: {ACCENT}; }}
.stage-done {{ border-color: {ACCENT_DIM}; }}
.stage-done .stage-idx::after {{ content: " ✓"; color: {ACCENT}; }}
.stage-error {{ border-color: {DANGER}; }}

.card {{
    border: 1px solid {PANEL_BORDER};
    background: {PANEL};
    border-radius: 14px;
    padding: 22px 24px;
}}
.card-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {ACCENT};
    margin-bottom: 10px;
}}

.log-line {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: {SUBTEXT};
    padding: 3px 0;
}}
.log-line .tag {{
    color: {ACCENT};
}}

.stButton > button, .stFormSubmitButton > button {{
    background: {ACCENT};
    color: #07120C;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    padding: 0.6rem 1.2rem;
    letter-spacing: 0.02em;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    background: #97FFC4;
    color: #07120C;
}}

.stTextInput > div > div > input {{
    background: {PANEL};
    border: 1px solid {PANEL_BORDER};
    color: {TEXT};
    border-radius: 9px;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: 1px solid {PANEL_BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: {SUBTEXT};
}}
.stTabs [aria-selected="true"] {{
    color: {ACCENT} !important;
}}

section[data-testid="stSidebar"] {{
    background: {PANEL};
    border-right: 1px solid {PANEL_BORDER};
}}

hr {{ border-color: {PANEL_BORDER}; }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PIPELINE DEFINITION
# ----------------------------------------------------------------------------
STAGES = [
    {"key": "search", "name": "Search Agent", "role": "Web reconnaissance"},
    {"key": "reader", "name": "Reader Agent", "role": "Source extraction"},
    {"key": "writer", "name": "Writer Chain", "role": "Report synthesis"},
    {"key": "critic", "name": "Critic Chain", "role": "Quality review"},
]


def render_pipeline(active_idx=-1, done_upto=-1, error_idx=-1):
    parts = ['<div class="pipeline-wrap">']
    for i, s in enumerate(STAGES):
        cls = "stage stage-pending"
        if i == error_idx:
            cls = "stage stage-error"
        elif i <= done_upto:
            cls = "stage stage-done"
        elif i == active_idx:
            cls = "stage stage-active"
        parts.append(
            f'<div class="{cls}">'
            f'<div class="stage-idx">STAGE {i+1:02d}</div>'
            f'<div class="stage-name">{s["name"]}</div>'
            f'<div class="stage-role">{s["role"]}</div>'
            f'</div>'
        )
    parts.append("</div>")
    return "".join(parts)


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace; color:{ACCENT}; font-size:0.75rem; letter-spacing:0.15em;">
    SYSTEM
    </div>
    <div style="font-weight:700; font-size:1.2rem; margin-bottom:18px;">Research Swarm</div>
    """, unsafe_allow_html=True)

    st.markdown("**Pipeline architecture**")
    for i, s in enumerate(STAGES):
        st.markdown(f"""
        <div style="display:flex; gap:10px; align-items:flex-start; margin-bottom:14px;">
            <div style="font-family:'JetBrains Mono',monospace; color:{ACCENT}; font-size:0.78rem;">{i+1:02d}</div>
            <div>
                <div style="font-weight:600; font-size:0.85rem;">{s['name']}</div>
                <div style="color:{SUBTEXT}; font-size:0.75rem;">{s['role']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("LangChain agents orchestrated sequentially: search → scrape → draft → critique.")

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent Research System</div>
    <div class="hero-title">🛰️ Research Swarm</div>
    <div class="hero-sub">Four specialized agents work in sequence — searching the web, scraping the best source,
    drafting a report, then critiquing it — to turn a single topic into a reviewed research brief.</div>
</div>
""", unsafe_allow_html=True)

if "state" not in st.session_state:
    st.session_state.state = None
if "logs" not in st.session_state:
    st.session_state.logs = []

# ----------------------------------------------------------------------------
# INPUT FORM
# ----------------------------------------------------------------------------
with st.form("research_form", clear_on_submit=False):
    c1, c2 = st.columns([5, 1])
    with c1:
        topic = st.text_input(
            "Research topic",
            placeholder="e.g. Latest advances in quantum error correction",
            label_visibility="collapsed",
        )
    with c2:
        submitted = st.form_submit_button("Run ▶", use_container_width=True)

pipeline_slot = st.empty()
if st.session_state.state is None and not submitted:
    pipeline_slot.markdown(render_pipeline(), unsafe_allow_html=True)

log_slot = st.empty()

# ----------------------------------------------------------------------------
# RUN PIPELINE
# ----------------------------------------------------------------------------
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        from Agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

        state = {}
        logs = []

        def log(msg):
            logs.append(msg)
            log_html = "".join(f'<div class="log-line"><span class="tag">›</span> {m}</div>' for m in logs)
            log_slot.markdown(f'<div class="card">{log_html}</div>', unsafe_allow_html=True)

        try:
            pipeline_slot.markdown(render_pipeline(active_idx=0), unsafe_allow_html=True)
            log("Search Agent dispatched — querying the web for recent, reliable sources...")
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content
            log("Search Agent complete — candidate sources gathered.")
            pipeline_slot.markdown(render_pipeline(active_idx=1, done_upto=0), unsafe_allow_html=True)

            log("Reader Agent dispatched — selecting and scraping the most relevant source...")
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            log("Reader Agent complete — deep content extracted.")
            pipeline_slot.markdown(render_pipeline(active_idx=2, done_upto=1), unsafe_allow_html=True)

            log("Writer Chain dispatched — drafting the report from combined research...")
            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
            log("Writer Chain complete — draft report ready.")
            pipeline_slot.markdown(render_pipeline(active_idx=3, done_upto=2), unsafe_allow_html=True)

            log("Critic Chain dispatched — reviewing the draft for quality and gaps...")
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            log("Critic Chain complete — review finalized.")
            pipeline_slot.markdown(render_pipeline(done_upto=3), unsafe_allow_html=True)

            log("✅ Pipeline finished successfully.")
            st.session_state.state = state
            st.session_state.logs = logs

        except Exception as e:
            pipeline_slot.markdown(render_pipeline(error_idx=len(logs) // 2 if logs else 0), unsafe_allow_html=True)
            log(f"❌ Pipeline failed: {e}")
            st.error(f"An error occurred: {e}")

# ----------------------------------------------------------------------------
# RESULTS
# ----------------------------------------------------------------------------
state = st.session_state.state
if state:
    st.markdown("<br>", unsafe_allow_html=True)
    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄  REPORT", "🧪  CRITIC REVIEW", "🔍  SEARCH RESULTS", "📚  SCRAPED CONTENT"]
    )

    def to_text(x):
        return x if isinstance(x, str) else str(x)

    with tab_report:
        report_text = to_text(state.get("report", ""))
        st.markdown(report_text)
        st.download_button("⬇ Download Report (.md)", data=report_text,
                            file_name="research_report.md", mime="text/markdown")

    with tab_feedback:
        st.markdown(to_text(state.get("feedback", "")))

    with tab_search:
        st.markdown(
            f'<div class="card"><pre style="white-space:pre-wrap; color:{SUBTEXT};">{to_text(state.get("search_results",""))}</pre></div>',
            unsafe_allow_html=True,
        )

    with tab_scraped:
        st.markdown(
            f'<div class="card"><pre style="white-space:pre-wrap; color:{SUBTEXT};">{to_text(state.get("scraped_content",""))}</pre></div>',
            unsafe_allow_html=True,
        )

elif not submitted:
    st.info("Enter a topic above and hit **Run ▶** to launch the agent swarm.")