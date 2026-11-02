# sidebar/filters.py — filtros de evento, dimensão, risk score e confiabilidade

import streamlit as st
import pandas as pd
from i18n import t
from keys import options_key


def render_filters(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    st.markdown("---")
    st.markdown(f"**{t('filters.header', lang)}**")

    event_names = df.drop_duplicates("EVENT_LETTER").set_index("EVENT_LETTER")["SHORT_EVENT"].to_dict()
    all_events = sorted(df["EVENT_LETTER"].unique())
    sel_events = st.multiselect(
        t("filters.events", lang), all_events, default=all_events,
        key=options_key("flt_events", all_events),
        format_func=lambda e: f"{e} — {event_names.get(e, '')}",
    )
    df = df[df["EVENT_LETTER"].isin(sel_events)]

    all_dims = sorted(df["DIM_LABEL"].unique())
    sel_dims = st.multiselect(t("filters.dimensions", lang), all_dims, default=all_dims,
                              key=options_key("flt_dims", all_dims))
    df = df[df["DIM_LABEL"].isin(sel_dims)]

    risk_range = st.slider(
        t("filters.risk_range", lang), -1.0, 1.0, (-1.0, 1.0), step=0.05, key="flt_risk",
    )
    df = df[
        (df["RISK_SCORE"] >= risk_range[0]) &
        (df["RISK_SCORE"] <= risk_range[1])
    ]

    min_trust = st.slider(t("filters.min_trust", lang), 0.0, 1.0, 0.0, step=0.05, key="flt_trust")
    df = df[df["TRUSTABILITY"] >= min_trust]

    return df
