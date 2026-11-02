# app.py — entry point
import streamlit as st
from config import GLOBAL_CSS
from i18n import t
from sidebar import render_sidebar
from sidebar.data_source import render_template_downloads
from views import TABS, detail_table

st.set_page_config(
    page_title="Risk Score Visualizer",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── sidebar + dados ────────────────────────────────────────────────────────────
df, controls = render_sidebar()
lang, texts = controls["lang"], controls["texts"]

if df is None:
    st.markdown(f"## {texts['page_title']}")
    st.caption(texts["page_subtitle"])
    st.info(t("landing.info", lang))
    st.markdown(t("landing.steps", lang))
    render_template_downloads(lang, prefix="main")
    st.stop()

if df.empty:
    st.warning(t("landing.empty_filters", lang))
    st.stop()

# ── header ─────────────────────────────────────────────────────────────────────
st.markdown(f"## {texts['page_title']}")
st.caption(texts["page_subtitle"])
st.markdown("")

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(t("kpi.events", lang),     df["EVENT_LETTER"].nunique())
k2.metric(t("kpi.dimensions", lang), len(df))
k3.metric(t("kpi.mean", lang),       f"{df['RISK_SCORE'].mean():+.3f}")
k4.metric(t("kpi.min", lang),        f"{df['RISK_SCORE'].min():+.3f}")
k5.metric(t("kpi.max", lang),        f"{df['RISK_SCORE'].max():+.3f}")

st.markdown("---")

# ── abas ───────────────────────────────────────────────────────────────────────
tabs = st.tabs([t(f"tab.{key}", lang) for key, _ in TABS])
for tab, (_, render) in zip(tabs, TABS):
    with tab:
        render(df, controls)

# ── tabela ──────────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander(f"🗂 {t('table.header', lang)}", expanded=False):
    detail_table(df, controls)
